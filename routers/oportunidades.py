from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db, Oportunidad as DBOportunidad, Empresa as DBEmpresa
from schemas.models import Oportunidad as SchemaOportunidad, OportunidadCreate, OportunidadUpdate
from security.core import get_current_user
from schemas.models import User as SchemaUser
from services.matching import calcular_compatibilidad
from db.database import Estudiante as DBEstudiante

router = APIRouter(prefix="/oportunidades", tags=["Oportunidades"])

@router.post("/", response_model=SchemaOportunidad, status_code=status.HTTP_201_CREATED)
async def create_oportunidad(
    oportunidad_create: OportunidadCreate,
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Crea una nueva oportunidad de trabajo. Solo para usuarios de tipo 'empresa'.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    if current_user.tipo != "empresa":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo las empresas pueden crear oportunidades."
        )

    # Obtener el perfil de la empresa del usuario actual
    empresa = db.query(DBEmpresa).filter(DBEmpresa.usuario_id == current_user.id).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de empresa no encontrado para el usuario actual."
        )

    try:
        db_oportunidad = DBOportunidad(
            **oportunidad_create.model_dump(),
            empresa_id=empresa.id
        )
        db.add(db_oportunidad)
        db.commit()
        db.refresh(db_oportunidad)
        return db_oportunidad
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear oportunidad: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al guardar la oferta: {str(e)}"
        )

@router.get("/", response_model=List[SchemaOportunidad])
async def get_all_oportunidades(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las oportunidades de trabajo activas.
    """
    oportunidades = db.query(DBOportunidad).filter(DBOportunidad.activa == True).all()
    return oportunidades

@router.get("/me", response_model=List[SchemaOportunidad])
async def get_my_oportunidades(
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Obtiene una lista de todas las oportunidades de trabajo publicadas por la empresa del usuario actual.
    """
    if current_user.tipo != "empresa":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo las empresas pueden ver sus oportunidades."
        )
    
    empresa = db.query(DBEmpresa).filter(DBEmpresa.usuario_id == current_user.id).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de empresa no encontrado."
        )

    return empresa.oportunidades

@router.get('/recomendadas/{estudiante_id}')
async def get_recomendadas(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Devuelve una lista de oportunidades activas junto con una puntuación de compatibilidad
    para el estudiante indicado.
    """
    estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

    oportunidades = db.query(DBOportunidad).filter(DBOportunidad.activa == True).all()

    recomendaciones = []
    for opp in oportunidades:
        try:
            score = calcular_compatibilidad(estudiante, opp)
        except Exception:
            score = 0.0
        
        # Obtener información de la empresa
        empresa_info = {}
        if opp.empresa:
            empresa_info = {
                "id": opp.empresa.id,
                "nombre": opp.empresa.nombre,
                "descripcion": opp.empresa.descripcion,
                "ubicacion": opp.empresa.ubicacion,
                "website": opp.empresa.website
            }
        
        recomendaciones.append({
            "oportunidad": {
                "id": opp.id,
                "empresa_id": opp.empresa_id,
                "empresa": empresa_info,
                "titulo": opp.titulo,
                "descripcion": opp.descripcion,
                "tipo": opp.tipo,
                "habilidades_requeridas": opp.habilidades_requeridas or [],
                "semestre_minimo": opp.semestre_minimo,
                "ubicacion": opp.ubicacion,
                "modalidad": opp.modalidad,
                "salario": opp.salario,
                "activa": opp.activa,
                "fecha_publicacion": opp.fecha_publicacion
            },
            "score": round(float(score), 2)
        })

    # Ordenar por score descendente
    recomendaciones.sort(key=lambda x: x['score'], reverse=True)
    return recomendaciones

@router.get("/{oportunidad_id}", response_model=SchemaOportunidad)
async def get_oportunidad_by_id(oportunidad_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una oportunidad de trabajo por su ID.
    """
    oportunidad = db.query(DBOportunidad).filter(DBOportunidad.id == oportunidad_id).first()
    if not oportunidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oportunidad no encontrada")
    return oportunidad

@router.patch("/{oportunidad_id}", response_model=SchemaOportunidad)
async def update_oportunidad(
    oportunidad_id: int,
    oportunidad_update: OportunidadUpdate,
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """

    Actualiza una oportunidad de trabajo. Solo la empresa que la creó puede actualizarla.
    """
    db_oportunidad = db.query(DBOportunidad).filter(DBOportunidad.id == oportunidad_id).first()
    if not db_oportunidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oportunidad no encontrada")

    # Verificar que el usuario es de la empresa que publicó la oportunidad
    if db_oportunidad.empresa.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta oportunidad."
        )

    update_data = oportunidad_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_oportunidad, key, value)

    db.commit()
    db.refresh(db_oportunidad)
    return db_oportunidad

@router.delete("/{oportunidad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_oportunidad(
    oportunidad_id: int,
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Elimina una oportunidad de trabajo. Solo la empresa que la creó puede eliminarla.
    """
    db_oportunidad = db.query(DBOportunidad).filter(DBOportunidad.id == oportunidad_id).first()
    if not db_oportunidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oportunidad no encontrada")

    if db_oportunidad.empresa.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta oportunidad."
        )

    db.delete(db_oportunidad)
    db.commit()
    return
