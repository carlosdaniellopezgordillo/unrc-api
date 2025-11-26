"""
Script para popular la base de datos con empresas y oportunidades ficticias.
Uso: python scripts/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, User, Empresa, Oportunidad, UserRole
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    # Verificar si ya existen empresas ficticias
    empresas_existentes = db.query(Empresa).count()
    if empresas_existentes > 0:
        print("✓ La base de datos ya contiene empresas. Abortando para no duplicar datos.")
        db.close()
        return
    
    # Crear usuarios empresa ficticios
    empresas_data = [
        {
            "nombre": "TechCorp Solutions",
            "email": "info@techcorp.com",
            "rfc": "TCO123456789",
            "sector": "Tecnología",
            "descripcion": "Líder en soluciones de software y consultoría tecnológica",
            "contacto": "Juan García",
            "telefono": "+34-91-123-4567",
            "direccion": "Calle Principal 123, Madrid"
        },
        {
            "nombre": "InnovaLabs",
            "email": "careers@innovalabs.com",
            "rfc": "INL234567890",
            "sector": "Inteligencia Artificial",
            "descripcion": "Empresa especializada en IA y machine learning",
            "contacto": "María López",
            "telefono": "+34-93-456-7890",
            "direccion": "Av. Diagonal 456, Barcelona"
        },
        {
            "nombre": "WebDesign Pro",
            "email": "hello@webdesignpro.com",
            "rfc": "WDP345678901",
            "sector": "Diseño y Desarrollo Web",
            "descripcion": "Especialistas en diseño UX/UI y desarrollo frontend",
            "contacto": "Carlos Martínez",
            "telefono": "+34-971-234-5678",
            "direccion": "Paseo Marítimo 789, Palma"
        },
        {
            "nombre": "DataViz Analytics",
            "email": "jobs@dataviz.com",
            "rfc": "DVA456789012",
            "sector": "Data Science",
            "descripcion": "Análisis de datos y visualización de información",
            "contacto": "Ana Rodríguez",
            "telefono": "+34-81-567-8901",
            "direccion": "Calle Digital 321, Sevilla"
        },
        {
            "nombre": "CloudNine Systems",
            "email": "recruit@cloudnine.com",
            "rfc": "CNS567890123",
            "sector": "Cloud Computing",
            "descripcion": "Infraestructura en la nube y DevOps",
            "contacto": "Pedro Sánchez",
            "telefono": "+34-914-567-8901",
            "direccion": "Av. Tecnológica 654, Madrid"
        },
        {
            "nombre": "MobileFirst Dev",
            "email": "contact@mobilefirst.com",
            "rfc": "MFD678901234",
            "sector": "Desarrollo Móvil",
            "descripcion": "Desarrollo de aplicaciones iOS y Android",
            "contacto": "Laura Fernández",
            "telefono": "+34-934-567-8901",
            "direccion": "Calle Móvil 987, Barcelona"
        },
        {
            "nombre": "CyberSecure Ltd",
            "email": "security@cybersecure.com",
            "rfc": "CSL789012345",
            "sector": "Ciberseguridad",
            "descripcion": "Soluciones de seguridad informática y auditoría",
            "contacto": "Raúl Gutiérrez",
            "telefono": "+34-91-234-5678",
            "direccion": "Calle Seguridad 111, Madrid"
        },
        {
            "nombre": "GreenTech Solutions",
            "email": "careers@greentech.com",
            "rfc": "GTS890123456",
            "sector": "Tecnología Sostenible",
            "descripcion": "Soluciones de energía renovable y sostenibilidad",
            "contacto": "Elena García",
            "telefono": "+34-81-234-5678",
            "direccion": "Parque Verde 222, Valencia"
        }
    ]
    
    # Crear empresas
    empresas_creadas = []
    for emp_data in empresas_data:
        # Crear usuario
        user = User(
            nombre=emp_data["contacto"].split()[0],
            apellido=" ".join(emp_data["contacto"].split()[1:]),
            email=emp_data["email"],
            hashed_password="dummy_hash",  # No se usará
            tipo=UserRole.empresa,
            activo=True
        )
        db.add(user)
        db.flush()
        
        # Crear empresa con nuevos campos
        empresa = Empresa(
            usuario_id=user.id,
            nombre=emp_data["nombre"],
            descripcion=emp_data["descripcion"],
            email_contacto=emp_data["email"],
            telefono=emp_data["telefono"],
            ubicacion=emp_data["direccion"],
            website=None,
            numero_empleados="50-100"
        )
        db.add(empresa)
        db.flush()
        empresas_creadas.append(empresa)
    
    db.commit()
    print(f"✓ {len(empresas_creadas)} empresas ficticias creadas")
    
    # Crear oportunidades ficticias
    oportunidades_data = [
        {
            "empresa_idx": 0,
            "titulo": "Desarrollador Full Stack Python + React",
            "descripcion": "Buscamos un desarrollador con experiencia en Python (Django/FastAPI) y React. Trabajarás en proyectos innovadores con el equipo de TechCorp.",
            "tipo": "empleo",
            "habilidades": ["Python", "React", "JavaScript", "SQL", "Git"],
            "semestre_minimo": 5,
            "gpa_minimo": 3.0,
            "ubicacion": "Madrid",
            "modalidad": "presencial",
            "duracion_meses": None,
            "salario": 28000
        },
        {
            "empresa_idx": 0,
            "titulo": "Prácticas en Desarrollo Backend",
            "descripcion": "Oportunidad de prácticas para estudiantes interesados en backend. Trabajarás con Python y bases de datos.",
            "tipo": "practica",
            "habilidades": ["Python", "SQL", "API REST"],
            "semestre_minimo": 3,
            "gpa_minimo": None,
            "ubicacion": "Madrid",
            "modalidad": "presencial",
            "duracion_meses": 6,
            "salario": None
        },
        {
            "empresa_idx": 1,
            "titulo": "Ingeniero de Machine Learning",
            "descripcion": "InnovaLabs busca ingenieros con experiencia en ML. Trabajarás con TensorFlow, PyTorch y grandes volúmenes de datos.",
            "tipo": "empleo",
            "habilidades": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Science"],
            "semestre_minimo": 6,
            "gpa_minimo": 3.5,
            "ubicacion": "Barcelona",
            "modalidad": "remoto",
            "duracion_meses": None,
            "salario": 35000
        },
        {
            "empresa_idx": 1,
            "titulo": "Servicio Social: Data Analysis",
            "descripcion": "Complementa tu formación con experiencia real en análisis de datos y visualización.",
            "tipo": "servicio_social",
            "habilidades": ["Python", "Pandas", "Matplotlib", "SQL"],
            "semestre_minimo": 4,
            "gpa_minimo": None,
            "ubicacion": "Barcelona",
            "modalidad": "hibrido",
            "duracion_meses": 4,
            "salario": None
        },
        {
            "empresa_idx": 2,
            "titulo": "Diseñador Frontend React",
            "descripcion": "Únete a nuestro equipo de diseño y desarrollo frontend. Crearás interfaces hermosas y funcionales.",
            "tipo": "empleo",
            "habilidades": ["React", "JavaScript", "CSS", "HTML", "Figma"],
            "semestre_minimo": 5,
            "gpa_minimo": 3.0,
            "ubicacion": "Palma",
            "modalidad": "presencial",
            "duracion_meses": None,
            "salario": 24000
        },
        {
            "empresa_idx": 2,
            "titulo": "Prácticas en UX/UI Design",
            "descripcion": "Aprende diseño de experiencia de usuario en un equipo profesional.",
            "tipo": "practica",
            "habilidades": ["Figma", "UI Design", "User Research"],
            "semestre_minimo": 3,
            "gpa_minimo": None,
            "ubicacion": "Palma",
            "modalidad": "presencial",
            "duracion_meses": 5,
            "salario": None
        },
        {
            "empresa_idx": 3,
            "titulo": "Analista de Datos Senior",
            "descripcion": "Posición senior para profesionales con experiencia en análisis de big data.",
            "tipo": "empleo",
            "habilidades": ["Python", "SQL", "Data Visualization", "Tableau", "Power BI"],
            "semestre_minimo": 7,
            "gpa_minimo": 3.2,
            "ubicacion": "Sevilla",
            "modalidad": "remoto",
            "duracion_meses": None,
            "salario": 32000
        },
        {
            "empresa_idx": 3,
            "titulo": "Prácticas en Business Intelligence",
            "descripcion": "Desarrolla habilidades en análisis de datos y reporting empresarial.",
            "tipo": "practica",
            "habilidades": ["SQL", "Power BI", "Excel"],
            "semestre_minimo": 4,
            "gpa_minimo": None,
            "ubicacion": "Sevilla",
            "modalidad": "hibrido",
            "duracion_meses": 4,
            "salario": None
        },
        {
            "empresa_idx": 4,
            "titulo": "DevOps Engineer",
            "descripcion": "Buscamos DevOps con experiencia en AWS, Docker y Kubernetes.",
            "tipo": "empleo",
            "habilidades": ["Docker", "Kubernetes", "AWS", "Git", "Linux"],
            "semestre_minimo": 6,
            "gpa_minimo": 3.1,
            "ubicacion": "Madrid",
            "modalidad": "presencial",
            "duracion_meses": None,
            "salario": 30000
        },
        {
            "empresa_idx": 4,
            "titulo": "Servicio Social: Cloud Infrastructure",
            "descripcion": "Aprende sobre infraestructura en la nube y automatización.",
            "tipo": "servicio_social",
            "habilidades": ["AWS", "Linux", "Python", "Bash"],
            "semestre_minimo": 5,
            "gpa_minimo": None,
            "ubicacion": "Madrid",
            "modalidad": "remoto",
            "duracion_meses": 5,
            "salario": None
        },
        {
            "empresa_idx": 5,
            "titulo": "Desarrollador iOS",
            "descripcion": "Desarrolla aplicaciones iOS innovadoras con Swift.",
            "tipo": "empleo",
            "habilidades": ["Swift", "iOS", "Objective-C", "Git"],
            "semestre_minimo": 5,
            "gpa_minimo": 3.0,
            "ubicacion": "Barcelona",
            "modalidad": "presencial",
            "duracion_meses": None,
            "salario": 26000
        },
        {
            "empresa_idx": 5,
            "titulo": "Prácticas en Desarrollo Android",
            "descripcion": "Aprende desarrollo de aplicaciones Android con Java y Kotlin.",
            "tipo": "practica",
            "habilidades": ["Android", "Kotlin", "Java"],
            "semestre_minimo": 4,
            "gpa_minimo": None,
            "ubicacion": "Barcelona",
            "modalidad": "presencial",
            "duracion_meses": 6,
            "salario": None
        },
        {
            "empresa_idx": 6,
            "titulo": "Especialista en Ciberseguridad",
            "descripcion": "Protege sistemas y redes contra amenazas cibernéticas.",
            "tipo": "empleo",
            "habilidades": ["Seguridad", "Redes", "Python", "Linux", "Penetration Testing"],
            "semestre_minimo": 6,
            "gpa_minimo": 3.3,
            "ubicacion": "Madrid",
            "modalidad": "presencial",
            "duracion_meses": None,
            "salario": 31000
        },
        {
            "empresa_idx": 6,
            "titulo": "Prácticas en Auditoría de Seguridad",
            "descripcion": "Aprende a realizar auditorías de seguridad informática.",
            "tipo": "practica",
            "habilidades": ["Seguridad", "Auditoría", "Redes"],
            "semestre_minimo": 5,
            "gpa_minimo": None,
            "ubicacion": "Madrid",
            "modalidad": "presencial",
            "duracion_meses": 4,
            "salario": None
        },
        {
            "empresa_idx": 7,
            "titulo": "Ingeniero de Energías Renovables",
            "descripcion": "Trabaja en proyectos de energía solar y eólica con tecnología IoT.",
            "tipo": "empleo",
            "habilidades": ["IoT", "Python", "Arduino", "Energías Renovables"],
            "semestre_minimo": 6,
            "gpa_minimo": 3.1,
            "ubicacion": "Valencia",
            "modalidad": "hibrido",
            "duracion_meses": None,
            "salario": 27000
        },
        {
            "empresa_idx": 7,
            "titulo": "Servicio Social: Sostenibilidad Tech",
            "descripcion": "Contribuye a un futuro sostenible con tecnología.",
            "tipo": "servicio_social",
            "habilidades": ["Python", "IoT", "Sostenibilidad"],
            "semestre_minimo": 4,
            "gpa_minimo": None,
            "ubicacion": "Valencia",
            "modalidad": "hibrido",
            "duracion_meses": 6,
            "salario": None
        }
    ]
    
    # Crear oportunidades
    for opp_data in oportunidades_data:
        empresa = empresas_creadas[opp_data["empresa_idx"]]
        
        fecha_cierre = datetime.now() + timedelta(days=30)
        
        oportunidad = Oportunidad(
            empresa_id=empresa.id,
            titulo=opp_data["titulo"],
            descripcion=opp_data["descripcion"],
            tipo=opp_data["tipo"],
            habilidades_requeridas=opp_data["habilidades"],
            semestre_minimo=opp_data["semestre_minimo"],
            gpa_minimo=opp_data.get("gpa_minimo"),
            ubicacion=opp_data["ubicacion"],
            modalidad=opp_data["modalidad"],
            duracion_meses=opp_data.get("duracion_meses"),
            salario=opp_data.get("salario"),
            fecha_cierre=fecha_cierre,
            activa=True
        )
        db.add(oportunidad)
    
    db.commit()
    print(f"✓ {len(oportunidades_data)} oportunidades ficticias creadas")
    
    print("\n✅ Base de datos populada exitosamente!")
    print(f"   - Empresas: {len(empresas_creadas)}")
    print(f"   - Oportunidades: {len(oportunidades_data)}")
    print("\nAhora puedes iniciar sesión y ver las oportunidades en la plataforma.")
    
    db.close()

if __name__ == "__main__":
    seed_data()
