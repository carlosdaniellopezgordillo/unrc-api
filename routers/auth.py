from fastapi import APIRouter, HTTPException, Depends, status, Body, Path
from fastapi.responses import JSONResponse
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Importaciones de módulos locales
from schemas.models import User, UserCreate, LoginRequest, Token, UserUpdate, TokenWithUser, UserInfo, Estudiante, EstudianteConUsuario
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from security.core import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from db.database import get_db, User as DBUser, Estudiante as DBEstudiante, Empresa as DBEmpresa

# --- Creación del Router ---
router = APIRouter(prefix="/auth", tags=["Authentication"])

"""
ADVERTENCIA DE PRIVACIDAD:
La información de los usuarios está protegida bajo los principios de confidencialidad, integridad y disponibilidad según la norma ISO/IEC 27001. El acceso, almacenamiento y tratamiento de datos personales está restringido y monitoreado. No compartas información sensible ni contraseñas a través de canales no autorizados.
"""


@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario (estudiante o empresa).
    - Si el rol es 'estudiante', se crea un perfil de estudiante vacío.
    - Si el rol es 'empresa', se crea un perfil de empresa vacío.
    """
    db_user = db.query(DBUser).filter(DBUser.email == user_create.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")

    # Para Argon2 usamos la contraseña como string (no es necesario truncarla).
    password_to_hash = user_create.password
    hashed_password = hash_password(password_to_hash)
    
    # Crear el usuario base
    db_user = DBUser(
        email=user_create.email,
        nombre=user_create.nombre,
        apellido=user_create.apellido,
        hashed_password=hashed_password,
        tipo=user_create.tipo  # Asignar el rol desde la petición
    )
    db.add(db_user)
    db.flush() # Para obtener el ID del usuario antes del commit

    # Crear el perfil específico según el rol
    if user_create.tipo == "estudiante":
        db_estudiante = DBEstudiante(usuario_id=db_user.id)
        db.add(db_estudiante)
    elif user_create.tipo == "empresa":
        # Crear perfil de empresa. En la tabla DBEmpresa el campo es `usuario_id`.
        db_empresa = DBEmpresa(usuario_id=db_user.id)
        db.add(db_empresa)

    db.commit()
    db.refresh(db_user)

    return UserInfo(id=db_user.id, nombre=db_user.nombre, tipo=db_user.tipo)

# --- Endpoint de Login ---
@router.post("/login", response_model=TokenWithUser)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener un token de acceso junto con la información del usuario.
    """
    db_user = db.query(DBUser).filter(DBUser.email == login_request.email).first()
    # Verificamos la contraseña tal cual (Argon2 espera str)
    password_to_verify = login_request.password
    if not db_user or not verify_password(password_to_verify, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)

    user_info = UserInfo(id=db_user.id, nombre=db_user.nombre, tipo=db_user.tipo)

    return {"access_token": access_token, "token_type": "bearer", "user": user_info}

# --- Endpoint para obtener todos los usuarios (protegido) ---
@router.get("/usuarios", response_model=List[User], tags=["Usuarios"])
async def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene una lista de todos los usuarios.
    Requiere autenticación.
    """
    if current_user.tipo != "administrador":
        raise HTTPException(status_code=403, detail="No tienes permiso para ver todos los usuarios.")
    
    users = db.query(DBUser).all()
    return users

# --- Endpoint público para obtener solo estudiantes ---
@router.get("/usuarios/estudiantes")
async def get_estudiantes(db: Session = Depends(get_db)):
    """
    Obtiene una lista pública de todos los estudiantes con su información completa.
    No requiere autenticación.
    """
    from db.database import Estudiante as DBEstudiante, User as DBUser
    try:
        # Obtener estudiantes con su información de usuario
        estudiantes = db.query(DBEstudiante).all()
        
        # Para cada estudiante, agregar manualmente la información del usuario
        resultado = []
        for est in estudiantes:
            usuario = db.query(DBUser).filter(DBUser.id == est.usuario_id).first()
            # Crear un diccionario con los datos del estudiante
            est_dict = {
                'id': est.id,
                'usuario_id': est.usuario_id,
                'matricula': est.matricula,
                'semestre': est.semestre,
                'carrera': est.carrera,
                'gpa': est.gpa,
                'habilidades_tecnicas': est.habilidades_tecnicas or [],
                'habilidades_blandas': est.habilidades_blandas or [],
                'proyectos': est.proyectos_lista or [],
                'disponibilidad': est.disponibilidad,
                'experiencias': est.experiencias or [],
                'habilidades': est.habilidades or [],
                'usuario': {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'email': usuario.email,
                    'tipo': usuario.tipo,
                    'activo': usuario.activo,
                    'fecha_creacion': str(usuario.fecha_creacion) if usuario.fecha_creacion else None
                } if usuario else None
            }
            resultado.append(est_dict)
        
        return resultado
    except Exception as e:
        import traceback
        print(f"Error en get_estudiantes: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes: {str(e)}")

# --- Endpoint para editar usuario (solo el propio usuario autenticado) ---
@router.patch("/usuarios/{usuario_id}", response_model=User, tags=["Usuarios"])
async def editar_usuario(usuario_id: int, datos: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Permite que solo el usuario autenticado edite su propia información.
    """
    if current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este usuario.")
    
    db_user = db.query(DBUser).filter(DBUser.id == usuario_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Actualiza solo los campos proporcionados
    update_data = datos.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)

    return db_user
