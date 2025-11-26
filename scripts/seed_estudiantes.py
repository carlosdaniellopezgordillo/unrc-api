#!/usr/bin/env python3
"""
Script para generar estudiantes ficticios en la base de datos.
"""
import sys
import os
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

# Añadir el directorio raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import User as DBUser, Estudiante as DBEstudiante, Base
from security.core import hash_password
from schemas.models import UserRole

# --- Configuración ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# --- Inicialización ---
fake = Faker('es_ES')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_estudiantes_ficticios(db):
    """Genera y guarda estudiantes ficticios en la base de datos."""
    
    carreras = [
        "Ingeniería en Sistemas",
        "Ciencias de Datos",
        "Ingeniería en Software",
        "Computación",
        "Informática",
        "Tecnologías de la Información",
        "Ingeniería Electrónica",
        "Ingeniería en Telecomunicaciones"
    ]
    
    habilidades_tecnicas_lista = [
        ["Python", "Django", "FastAPI"],
        ["JavaScript", "React", "Node.js"],
        ["Java", "Spring Boot", "SQL"],
        ["Python", "Machine Learning", "TensorFlow"],
        ["SQL", "PostgreSQL", "MongoDB"],
        ["Docker", "Kubernetes", "AWS"],
        ["C++", "Programación Competitiva"],
        ["PHP", "Laravel", "MySQL"],
        ["Go", "Rust", "sistemas operativos"],
        ["Cloud Computing", "Azure", "GCP"],
        ["Frontend", "CSS", "UI/UX"],
        ["Backend", "APIs", "REST"],
        ["DevOps", "Linux", "GitHub Actions"],
        ["Data Analysis", "Power BI", "Excel"],
        ["Mobile Development", "Flutter", "Kotlin"]
    ]
    
    habilidades_blandas_lista = [
        ["Comunicación", "Trabajo en equipo"],
        ["Liderazgo", "Resolución de problemas"],
        ["Creatividad", "Pensamiento crítico"],
        ["Adaptabilidad", "Aprendizaje rápido"],
        ["Empatía", "Negociación"],
        ["Gestión de tiempo", "Organización"],
        ["Presentación", "Escritura"],
        ["Mentoría", "Colaboración"]
    ]
    
    proyectos_lista = [
        "Sistema de Gestión de Inventario",
        "Aplicación de E-commerce",
        "Red Social Académica",
        "Bot de Discord",
        "Análisis de Redes Sociales",
        "Plataforma de Learning",
        "API REST para Blog",
        "Juego 2D en Python",
        "Dashboard de Analytics",
        "Chatbot con IA",
        "Aplicación Móvil",
        "Gestor de Tareas",
        "Sistema de Reservas",
        "Marketplace Local",
        "Plataforma de Cursos"
    ]
    
    estudiantes_creados = 0
    for i in range(15):  # Crear 15 estudiantes
        try:
            nombre = fake.first_name()
            apellido = fake.last_name()
            email = f"{nombre.lower()}.{apellido.lower()}{i}@unrc.edu.mx"
            
            # Verificar si existe
            if db.query(DBUser).filter(DBUser.email == email).first():
                continue
            
            # Crear usuario estudiante
            hashed_pwd = hash_password("estudiante123")
            nuevo_usuario = DBUser(
                email=email,
                nombre=nombre,
                apellido=apellido,
                tipo=UserRole.estudiante,
                hashed_password=hashed_pwd,
                activo=True
            )
            db.add(nuevo_usuario)
            db.flush()
            
            # Crear perfil estudiante
            nuevo_estudiante = DBEstudiante(
                usuario_id=nuevo_usuario.id,
                matricula=f"MAT{random.randint(100000, 999999)}",
                semestre=random.randint(1, 10),
                carrera=random.choice(carreras),
                gpa=round(random.uniform(2.5, 4.0), 2),
                habilidades_tecnicas=random.choice(habilidades_tecnicas_lista),
                habilidades_blandas=random.choice(habilidades_blandas_lista),
                proyectos_lista=random.sample(proyectos_lista, random.randint(2, 4)),
                disponibilidad=random.choice([True, True, True, False])  # 75% disponibles
            )
            db.add(nuevo_estudiante)
            db.commit()
            estudiantes_creados += 1
            print(f"✅ Estudiante '{nombre} {apellido}' creado - {nuevo_estudiante.carrera} (Semestre {nuevo_estudiante.semestre})")
            
        except Exception as e:
            print(f"❌ Error creando estudiante: {e}")
            db.rollback()
            continue
    
    print(f"\n✅ Se crearon {estudiantes_creados} estudiantes ficticios")
    return estudiantes_creados

def main():
    print("=" * 80)
    print("SEEDING DE ESTUDIANTES FICTICIOS")
    print("=" * 80)
    
    try:
        db = SessionLocal()
        
        print("\n1️⃣  Creando estudiantes ficticios...")
        crear_estudiantes_ficticios(db)
        
        print("\n" + "=" * 80)
        print("✅ SEEDING COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error durante el seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
