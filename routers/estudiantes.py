from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
from db.database import get_db, Estudiante as DBEstudiante, Experiencia as DBExperiencia, User as DBUser
from services.cv_parser import parse_cv
from fastapi.responses import FileResponse
from security.core import get_current_user
from schemas.models import User as SchemaUser

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

UPLOAD_DIR = "uploaded_cvs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/me/profile", status_code=status.HTTP_200_OK)
def get_my_profile(db: Session = Depends(get_db), current_user: SchemaUser = Depends(get_current_user)):
    """
    Obtiene el perfil del estudiante autenticado por usuario_id.
    """
    if current_user.tipo != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden acceder a esto")
    
    db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.usuario_id == current_user.id).first()
    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return {
        "id": db_estudiante.id,
        "usuario_id": db_estudiante.usuario_id,
        "matricula": db_estudiante.matricula,
        "semestre": db_estudiante.semestre,
        "carrera": db_estudiante.carrera,
        "gpa": db_estudiante.gpa,
        "habilidades_tecnicas": db_estudiante.habilidades_tecnicas or [],
        "habilidades_blandas": db_estudiante.habilidades_blandas or [],
        "proyectos": db_estudiante.proyectos_lista or [],
        "experiencias": [
            {"puesto": e.puesto, "empresa": e.empresa, "descripcion": e.descripcion, "fecha_inicio": e.fecha_inicio, "fecha_fin": e.fecha_fin} for e in db_estudiante.experiencias
        ],
        "cv_path": db_estudiante.cv_path,
    }

@router.post("/me/upload_cv", status_code=status.HTTP_200_OK)
async def upload_cv_me(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: SchemaUser = Depends(get_current_user)):
    """
    Permite al estudiante autenticado subir su CV.
    Busca el perfil de estudiante por usuario_id.
    """
    if current_user.tipo != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden subir CV")
    
    try:
        import json
        db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.usuario_id == current_user.id).first()
        if not db_estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".doc", ".docx"]:
            raise HTTPException(status_code=400, detail="Formato de archivo no permitido. Use PDF, DOC o DOCX")
        
        # Crear directorio si no existe
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        save_path = os.path.join(UPLOAD_DIR, f"cv_{db_estudiante.id}{ext}")
        
        # Leer y guardar archivo
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        with open(save_path, "wb") as f:
            f.write(contents)
        
        db_estudiante.cv_path = save_path
        
        # Intentar parsear el CV para extraer información
        parsed = parse_cv(save_path)
        
        # Actualizar campos en la base de datos si se encontraron, evitando duplicados
        if parsed.get('carrera'):
            db_estudiante.carrera = parsed.get('carrera')
        
        if parsed.get('habilidades'):
            # Mezclar con existentes y eliminar duplicados (case-insensitive)
            existing_skills = db_estudiante.habilidades_tecnicas or []
            existing_skills_lower = [s.lower() for s in existing_skills]
            new_skills = [
                h for h in parsed.get('habilidades') 
                if h.lower() not in existing_skills_lower
            ]
            db_estudiante.habilidades_tecnicas = list(set(existing_skills + new_skills))
        
        if parsed.get('proyectos'):
            # Mezclar con existentes y eliminar duplicados
            existing_projects = db_estudiante.proyectos_lista or []
            new_projects = [
                p for p in parsed.get('proyectos')
                if p not in existing_projects
            ]
            db_estudiante.proyectos_lista = list(set(existing_projects + new_projects))
        
        # Crear experiencias extraídas (si hay), evitando duplicados
        if parsed.get('experiencias'):
            existing_descriptions = {e.descripcion for e in db_estudiante.experiencias}
            for exp_text in parsed.get('experiencias'):
                if exp_text not in existing_descriptions:
                    exp = DBExperiencia(
                        puesto=exp_text[:150], 
                        empresa='', 
                        descripcion=exp_text, 
                        estudiante_id=db_estudiante.id
                    )
                    db.add(exp)
        
        db.commit()
        
        # Retornar los datos parseados limpios (sin duplicados)
        return {
            "message": "CV subido y procesado correctamente", 
            "cv_path": save_path, 
            "parsed": {
                "carrera": parsed.get('carrera'),
                "habilidades": list(set(parsed.get('habilidades', []))),
                "proyectos": list(set(parsed.get('proyectos', []))),
                "experiencias": list(set(parsed.get('experiencias', [])))
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar CV: {str(e)}")

@router.patch("/me/perfil", status_code=status.HTTP_200_OK)
async def update_my_perfil(
    carrera: str = Form(None),
    semestre: int = Form(None),
    habilidades_tecnicas: str = Form(None),
    habilidades_blandas: str = Form(None),
    proyectos: str = Form(None),
    experiencias: str = Form(None),
    db: Session = Depends(get_db),
    current_user: SchemaUser = Depends(get_current_user)
):
    """
    Permite al estudiante autenticado editar su perfil: carrera, semestre, skills, proyectos, experiencia laboral.
    Los datos se envían como JSON serializado en string.
    """
    if current_user.tipo != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden editar su perfil")
    
    try:
        import json
        import traceback
        
        db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.usuario_id == current_user.id).first()
        if not db_estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Actualizar carrera y semestre
        if carrera is not None and carrera != '':
            db_estudiante.carrera = str(carrera).strip()
        if semestre is not None and semestre != '':
            try:
                db_estudiante.semestre = int(semestre)
            except (ValueError, TypeError):
                pass
        
        # Actualizar habilidades técnicas
        if habilidades_tecnicas:
            try:
                tech_skills = json.loads(habilidades_tecnicas)
                if isinstance(tech_skills, list):
                    db_estudiante.habilidades_tecnicas = [str(s).strip() for s in tech_skills if s]
                else:
                    db_estudiante.habilidades_tecnicas = []
            except:
                db_estudiante.habilidades_tecnicas = []
        
        # Actualizar habilidades blandas
        if habilidades_blandas:
            try:
                soft_skills = json.loads(habilidades_blandas)
                if isinstance(soft_skills, list):
                    db_estudiante.habilidades_blandas = [str(s).strip() for s in soft_skills if s]
                else:
                    db_estudiante.habilidades_blandas = []
            except:
                db_estudiante.habilidades_blandas = []
        
        # Actualizar proyectos
        if proyectos:
            try:
                projects_list = json.loads(proyectos)
                if isinstance(projects_list, list):
                    db_estudiante.proyectos_lista = [str(p).strip() for p in projects_list if p]
                else:
                    db_estudiante.proyectos_lista = []
            except:
                db_estudiante.proyectos_lista = []
        
        # Manejar experiencias: son objetos relacionados, no un campo JSON
        if experiencias:
            try:
                experiencias_data = json.loads(experiencias) if isinstance(experiencias, str) else []
                
                # Limpiar todas las experiencias previas
                db.query(DBExperiencia).filter(
                    DBExperiencia.estudiante_id == db_estudiante.id
                ).delete(synchronize_session=False)
                
                # Crear nuevas experiencias desde el frontend
                if isinstance(experiencias_data, list):
                    for exp_data in experiencias_data:
                        if isinstance(exp_data, dict) and (exp_data.get('puesto') or exp_data.get('descripcion')):
                            try:
                                puesto = str(exp_data.get('puesto', '')).strip()[:150]
                                empresa = str(exp_data.get('empresa', '')).strip()[:150]
                                descripcion = str(exp_data.get('descripcion', '')).strip()[:500]
                                
                                if puesto or descripcion:
                                    exp = DBExperiencia(
                                        puesto=puesto,
                                        empresa=empresa,
                                        descripcion=descripcion,
                                        fecha_inicio=None,
                                        fecha_fin=None,
                                        estudiante_id=db_estudiante.id
                                    )
                                    db.add(exp)
                            except Exception as exp_err:
                                print(f"Error creando experiencia: {exp_err}")
                                traceback.print_exc()
                                continue
            except json.JSONDecodeError:
                # Si no es JSON válido, ignorar experiencias
                pass
            except Exception as exp_err:
                print(f"Error general en experiencias: {exp_err}")
                traceback.print_exc()
        
        db.commit()
        return {"message": "Perfil actualizado correctamente"}
        
    except Exception as e:
        db.rollback()
        print(f"Error en update_my_perfil: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al actualizar perfil: {str(e)}")

@router.post("/{estudiante_id}/upload_cv", status_code=status.HTTP_200_OK)
async def upload_cv(estudiante_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Permite a un estudiante subir su CV (PDF/DOCX).
    Guarda la ruta del archivo en la base de datos.
    Evita duplicación de información si se sube múltiples veces.
    """
    try:
        import json
        db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
        if not db_estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".doc", ".docx"]:
            raise HTTPException(status_code=400, detail="Formato de archivo no permitido. Use PDF, DOC o DOCX")
        
        # Crear directorio si no existe
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        save_path = os.path.join(UPLOAD_DIR, f"cv_{estudiante_id}{ext}")
        
        # Leer y guardar archivo
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        with open(save_path, "wb") as f:
            f.write(contents)
        
        db_estudiante.cv_path = save_path
        
        # Intentar parsear el CV para extraer información
        parsed = parse_cv(save_path)
        
        # Actualizar campos en la base de datos si se encontraron, evitando duplicados
        if parsed.get('carrera'):
            db_estudiante.carrera = parsed.get('carrera')
        
        if parsed.get('habilidades'):
            # Mezclar con existentes y eliminar duplicados (case-insensitive)
            existing_skills = db_estudiante.habilidades_tecnicas or []
            existing_skills_lower = [s.lower() for s in existing_skills]
            new_skills = [
                h for h in parsed.get('habilidades') 
                if h.lower() not in existing_skills_lower
            ]
            db_estudiante.habilidades_tecnicas = list(set(existing_skills + new_skills))
        
        if parsed.get('proyectos'):
            # Mezclar con existentes y eliminar duplicados
            existing_projects = db_estudiante.proyectos_lista or []
            new_projects = [
                p for p in parsed.get('proyectos')
                if p not in existing_projects
            ]
            db_estudiante.proyectos_lista = list(set(existing_projects + new_projects))
        
        # Crear experiencias extraídas (si hay), evitando duplicados
        if parsed.get('experiencias'):
            existing_descriptions = {e.descripcion for e in db_estudiante.experiencias}
            for exp_text in parsed.get('experiencias'):
                if exp_text not in existing_descriptions:
                    exp = DBExperiencia(
                        puesto=exp_text[:150], 
                        empresa='', 
                        descripcion=exp_text, 
                        estudiante_id=db_estudiante.id
                    )
                    db.add(exp)
        
        db.commit()
        
        # Retornar los datos parseados limpios (sin duplicados)
        return {
            "message": "CV subido y procesado correctamente", 
            "cv_path": save_path, 
            "parsed": {
                "carrera": parsed.get('carrera'),
                "habilidades": list(set(parsed.get('habilidades', []))),
                "proyectos": list(set(parsed.get('proyectos', []))),
                "experiencias": list(set(parsed.get('experiencias', [])))
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar CV: {str(e)}")


@router.get("/{estudiante_id}", status_code=status.HTTP_200_OK)
def get_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la información del estudiante por su id.
    """
    db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Serializar campos relevantes
    return {
        "id": db_estudiante.id,
        "usuario_id": db_estudiante.usuario_id,
        "matricula": db_estudiante.matricula,
        "semestre": db_estudiante.semestre,
        "carrera": db_estudiante.carrera,
        "gpa": db_estudiante.gpa,
        "habilidades_tecnicas": db_estudiante.habilidades_tecnicas or [],
        "habilidades_blandas": db_estudiante.habilidades_blandas or [],
        "proyectos": db_estudiante.proyectos_lista or [],
        "experiencias": [
            {"puesto": e.puesto, "empresa": e.empresa, "descripcion": e.descripcion, "fecha_inicio": e.fecha_inicio, "fecha_fin": e.fecha_fin} for e in db_estudiante.experiencias
        ],
        "cv_path": db_estudiante.cv_path,
    }


@router.get("/{estudiante_id}/public", status_code=status.HTTP_200_OK)
def get_estudiante_public(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Endpoint público pensado para que empresas consulten el perfil del estudiante.
    No incluye datos sensibles; devuelve nombre, carrera, habilidades, proyectos, experiencias y enlace al CV.
    """
    db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    # obtener nombre de usuario
    usuario = db.query(DBUser).filter(DBUser.id == db_estudiante.usuario_id).first()
    nombre = f"{usuario.nombre} {getattr(usuario, 'apellido', '')}" if usuario else None

    experiencias = [
        {"id": e.id, "puesto": e.puesto, "empresa": e.empresa, "descripcion": e.descripcion, "fecha_inicio": e.fecha_inicio, "fecha_fin": e.fecha_fin}
        for e in db_estudiante.experiencias
    ]

    return {
        "id": db_estudiante.id,
        "nombre": nombre,
        "carrera": db_estudiante.carrera,
        "habilidades_tecnicas": db_estudiante.habilidades_tecnicas or [],
        "proyectos": db_estudiante.proyectos_lista or [],
        "experiencias": experiencias,
        "cv_download": f"/estudiantes/{db_estudiante.id}/cv/download" if db_estudiante.cv_path else None
    }


@router.get("/{estudiante_id}/cv/download", status_code=status.HTTP_200_OK)
def download_cv(estudiante_id: int, db: Session = Depends(get_db)):
    """Devuelve el archivo del CV para descarga si existe."""
    db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
    if not db_estudiante or not db_estudiante.cv_path:
        raise HTTPException(status_code=404, detail="CV no encontrado")
    return FileResponse(path=db_estudiante.cv_path, filename=os.path.basename(db_estudiante.cv_path))

@router.patch("/{estudiante_id}/perfil", status_code=status.HTTP_200_OK)
async def update_perfil(
    estudiante_id: int,
    habilidades_tecnicas: str = Form(None),
    habilidades_blandas: str = Form(None),
    proyectos: str = Form(None),
    experiencias: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Permite editar el perfil del estudiante: skills, proyectos, experiencia laboral.
    Los datos se envían como JSON serializado en string.
    """
    try:
        import json
        db_estudiante = db.query(DBEstudiante).filter(DBEstudiante.id == estudiante_id).first()
        if not db_estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        if habilidades_tecnicas:
            db_estudiante.habilidades_tecnicas = json.loads(habilidades_tecnicas)
        if habilidades_blandas:
            db_estudiante.habilidades_blandas = json.loads(habilidades_blandas)
        if proyectos:
            db_estudiante.proyectos_lista = json.loads(proyectos)
        
        # Manejar experiencias: son objetos relacionados, no un campo JSON
        if experiencias:
            experiencias_data = json.loads(experiencias)
            
            # Limpiar experiencias previas que vinieron del parsing
            existing_exp = db.query(DBExperiencia).filter(
                DBExperiencia.estudiante_id == estudiante_id,
                DBExperiencia.empresa == ''  # Solo las que fueron parseadas
            ).all()
            for exp in existing_exp:
                db.delete(exp)
            
            # Crear nuevas experiencias desde el frontend
            for exp_data in experiencias_data:
                if isinstance(exp_data, dict):
                    exp = DBExperiencia(
                        puesto=exp_data.get('puesto', '')[:150],
                        empresa=exp_data.get('empresa', ''),
                        descripcion=exp_data.get('descripcion', ''),
                        estudiante_id=estudiante_id
                    )
                    db.add(exp)
                elif isinstance(exp_data, str) and exp_data.strip():
                    # Si es string, crear como descripción
                    exp = DBExperiencia(
                        puesto=exp_data[:150],
                        empresa='',
                        descripcion=exp_data,
                        estudiante_id=estudiante_id
                    )
                    db.add(exp)
        
        db.commit()
        return {"message": "Perfil actualizado correctamente"}
    except json.JSONDecodeError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al procesar JSON: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar perfil: {str(e)}")
