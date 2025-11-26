from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import database
from schemas import models
from security import core

router = APIRouter(
    prefix="/habilidades",
    tags=["Habilidades"]
)

# Endpoint para crear una nueva habilidad en el sistema (para administradores, quizás)
@router.post("/", response_model=models.Habilidad)
def create_habilidad(habilidad: models.HabilidadCreate, db: Session = Depends(database.get_db)):
    db_habilidad = db.query(database.Habilidad).filter(database.Habilidad.nombre == habilidad.nombre).first()
    if db_habilidad:
        raise HTTPException(status_code=400, detail="Habilidad ya registrada")
    new_habilidad = database.Habilidad(nombre=habilidad.nombre)
    db.add(new_habilidad)
    db.commit()
    db.refresh(new_habilidad)
    return new_habilidad

# Endpoint para obtener todas las habilidades
@router.get("/", response_model=List[models.Habilidad])
def get_habilidades(db: Session = Depends(database.get_db)):
    return db.query(database.Habilidad).all()

# Endpoint para que un estudiante agregue una habilidad a su perfil
@router.post("/me/{habilidad_id}", response_model=models.User)
def add_habilidad_to_current_user(
    habilidad_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(core.get_current_user)
):
    # Asumiendo que el usuario tiene un perfil de estudiante creado.
    # Se necesitará lógica adicional al registrar un usuario para crear su perfil de estudiante.
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado para el usuario actual")

    habilidad = db.query(database.Habilidad).filter(database.Habilidad.id == habilidad_id).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")

    if habilidad in estudiante.habilidades:
        raise HTTPException(status_code=400, detail="El estudiante ya tiene esta habilidad")

    estudiante.habilidades.append(habilidad)
    db.commit()
    db.refresh(current_user)
    return current_user

# Endpoint para que un estudiante elimine una habilidad de su perfil
@router.delete("/me/{habilidad_id}", response_model=models.User)
def remove_habilidad_from_current_user(
    habilidad_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    habilidad = db.query(database.Habilidad).filter(database.Habilidad.id == habilidad_id).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")

    if habilidad not in estudiante.habilidades:
        raise HTTPException(status_code=400, detail="El estudiante no tiene esta habilidad")

    estudiante.habilidades.remove(habilidad)
    db.commit()
    db.refresh(current_user)
    return current_user
