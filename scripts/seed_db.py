import sys
import os
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Añadir el directorio raíz del proyecto al sys.path
# Esto es necesario para que el script pueda encontrar los módulos de la aplicación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import User as DBUser, Estudiante as DBEstudiante, Base
from security.core import hash_password
from schemas.models import UserRole

# --- Configuración ---
# Construir la ruta absoluta a la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
NUM_ESTUDIANTES = 50  # Número de estudiantes a generar

# --- Inicialización ---
fake = Faker('es_ES') # Usar localización en español para nombres más comunes en la región
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Funciones de Generación de Datos ---

def crear_estudiantes_ficticios(db):
    """Genera y guarda estudiantes ficticios en la base de datos."""
    
    # Listas de ejemplo para datos aleatorios
    carreras = ["Ciencias de Datos para Negocios", "Ingeniería de Software", "Animación y Efectos Visuales", "Seguridad Informática"]
    habilidades_tecnicas = ["Python", "SQL", "Power BI", "Tableau", "Machine Learning", "React", "Node.js", "MongoDB", "Git"]
    habilidades_blandas = ["Comunicación", "Trabajo en equipo", "Resolución de problemas", "Liderazgo", "Adaptabilidad"]

    estudiantes_creados = 0
    for i in range(NUM_ESTUDIANTES):
        try:
            nombre = fake.first_name()
            apellido = fake.last_name()
            email = f"{nombre.lower()}.{apellido.lower()}{i}@edu.unrc.mx"
            
            # Verificar si el email ya existe
            if db.query(DBUser).filter(DBUser.email == email).first():
                continue

            # 1. Crear el usuario base
            hashed_pwd = hash_password("password123") # Contraseña simple para todos los fakes
            nuevo_usuario = DBUser(
                email=email,
                nombre=nombre,
                apellido=apellido,
                tipo=UserRole.estudiante,
                hashed_password=hashed_pwd,
                activo=True
            )
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)

            # 2. Crear el perfil de estudiante asociado
            tech_skills = random.sample(habilidades_tecnicas, k=random.randint(3, 6))
            soft_skills = random.sample(habilidades_blandas, k=random.randint(2, 4))
            projects = [fake.bs().title() for _ in range(random.randint(1, 3))]
            
            print(f"Tech skills type: {type(tech_skills)}, value: {tech_skills}")
            print(f"Soft skills type: {type(soft_skills)}, value: {soft_skills}")
            print(f"Projects type: {type(projects)}, value: {projects}")
            
            nuevo_estudiante = DBEstudiante(
                usuario_id=nuevo_usuario.id,
                matricula=f"A{fake.unique.random_number(digits=8)}",
                semestre=random.randint(6, 9),
                carrera=random.choice(carreras),
                gpa=round(random.uniform(7.5, 9.8), 2),
                habilidades_tecnicas=tech_skills,
                habilidades_blandas=soft_skills,
                proyectos_lista=projects,
                disponibilidad=random.choice([True, True, False])
            )
            print(f"About to add estudiante: {nuevo_estudiante}")
            db.add(nuevo_estudiante)
            db.commit()
            estudiantes_creados += 1
        except Exception as e:
            print(f"Error creando estudiante {i}: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            continue

    print(f"✅ ¡Se han creado {estudiantes_creados} estudiantes ficticios con éxito!")

# --- Ejecución del Script ---
if __name__ == "__main__":
    print("Iniciando el proceso de seeding para la base de datos...")
    
    # Crear tablas si no existen (importante para la primera ejecución)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        crear_estudiantes_ficticios(db)
    except Exception as e:
        print(f"❌ Error durante el seeding: {e}")
        db.rollback()
    finally:
        db.close()
        print("Proceso de seeding finalizado.")
