from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import database
from schemas import models
from security import core

router = APIRouter(
    prefix="/experiencias",
    tags=["Experiencias"]
)

# Endpoint para que un estudiante agregue una experiencia a su perfil
@router.post("/me", response_model=models.Experiencia)
def add_experiencia_to_current_user(
    experiencia: models.ExperienciaCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    new_experiencia = database.Experiencia(**experiencia.model_dump(), estudiante_id=estudiante.id)
    db.add(new_experiencia)
    db.commit()
    db.refresh(new_experiencia)
    return new_experiencia

# Endpoint para que un estudiante actualice una de sus experiencias
@router.put("/me/{experiencia_id}", response_model=models.Experiencia)
def update_experiencia_for_current_user(
    experiencia_id: int,
    experiencia_update: models.ExperienciaCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    db_experiencia = db.query(database.Experiencia).filter(
        database.Experiencia.id == experiencia_id,
        database.Experiencia.estudiante_id == estudiante.id
    ).first()

    if not db_experiencia:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")

    for var, value in experiencia_update.model_dump(exclude_unset=True).items():
        setattr(db_experiencia, var, value)
    
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia

# Endpoint para que un estudiante elimine una de sus experiencias
@router.delete("/me/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiencia_from_current_user(
    experiencia_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    db_experiencia = db.query(database.Experiencia).filter(
        database.Experiencia.id == experiencia_id,
        database.Experiencia.estudiante_id == estudiante.id
    ).first()

    if not db_experiencia:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")

    db.delete(db_experiencia)
    db.commit()
    return {"ok": True}
