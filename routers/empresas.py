from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db, Empresa as DBEmpresa
from schemas.models import Empresa as SchemaEmpresa, EmpresaUpdate
from security.core import get_current_user
from schemas.models import User as SchemaUser

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get("/", response_model=List[SchemaEmpresa])
async def get_all_empresas(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los perfiles de empresa.
    """
    empresas = db.query(DBEmpresa).all()
    return empresas

@router.get("/me", response_model=SchemaEmpresa)
async def get_my_empresa_profile(
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Obtiene el perfil de empresa del usuario autenticado.
    """
    if current_user.tipo != "empresa":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción no permitida. Solo los usuarios de tipo 'empresa' pueden acceder a esto."
        )

    db_empresa = db.query(DBEmpresa).filter(DBEmpresa.usuario_id == current_user.id).first()
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de empresa no encontrado."
        )
    return db_empresa

@router.get("/{empresa_id}", response_model=SchemaEmpresa)
async def get_empresa_by_id(empresa_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el perfil de una empresa por su ID.
    """
    empresa = db.query(DBEmpresa).filter(DBEmpresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    return empresa

@router.patch("/me", response_model=SchemaEmpresa)
async def update_my_empresa_profile(
    empresa_update: EmpresaUpdate,
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Permite a un usuario de tipo 'empresa' actualizar su propio perfil.
    """
    if current_user.tipo != "empresa":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acción no permitida. Solo los usuarios de tipo 'empresa' pueden modificar su perfil."
        )

    # Buscar el perfil de empresa asociado al usuario actual
    db_empresa = db.query(DBEmpresa).filter(DBEmpresa.usuario_id == current_user.id).first()
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de empresa no encontrado para el usuario actual."
        )

    # Actualizar los campos proporcionados
    update_data = empresa_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empresa, key, value)

    db.commit()
    db.refresh(db_empresa)
    return db_empresa
