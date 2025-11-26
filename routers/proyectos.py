from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import database
from schemas import models
from security import core

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"]
)

# Endpoint para que un estudiante agregue un proyecto a su perfil
@router.post("/me", response_model=models.Proyecto)
def add_proyecto_to_current_user(
    proyecto: models.ProyectoCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    new_proyecto = database.Proyecto(**proyecto.model_dump(), estudiante_id=estudiante.id)
    db.add(new_proyecto)
    db.commit()
    db.refresh(new_proyecto)
    return new_proyecto

# Endpoint para que un estudiante actualice uno de sus proyectos
@router.put("/me/{proyecto_id}", response_model=models.Proyecto)
def update_proyecto_for_current_user(
    proyecto_id: int,
    proyecto_update: models.ProyectoCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    db_proyecto = db.query(database.Proyecto).filter(
        database.Proyecto.id == proyecto_id,
        database.Proyecto.estudiante_id == estudiante.id
    ).first()

    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    for var, value in proyecto_update.model_dump(exclude_unset=True).items():
        setattr(db_proyecto, var, value)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

# Endpoint para que un estudiante elimine uno de sus proyectos
@router.delete("/me/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proyecto_from_current_user(
    proyecto_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(core.get_current_user)
):
    estudiante = current_user.estudiante
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")

    db_proyecto = db.query(database.Proyecto).filter(
        database.Proyecto.id == proyecto_id,
        database.Proyecto.estudiante_id == estudiante.id
    ).first()

    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    db.delete(db_proyecto)
    db.commit()
    return {"ok": True}
