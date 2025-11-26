import sys
import os
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Añadir el directorio raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import User as DBUser, Empresa as DBEmpresa, Oportunidad as DBOportunidad, Base
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

def crear_empresas_ficticias(db):
    """Genera y guarda empresas ficticias en la base de datos."""
    
    empresas_nombres = [
        "Tech Innovations Inc",
        "DataDriven Solutions",
        "CloudNet Systems",
        "AI Futures Lab",
        "Web Dynamics Co",
        "Analytics Pro",
        "DevOps Masters",
        "Mobile First",
        "Security Plus",
        "Database World"
    ]
    
    empresas_creadas = 0
    for nombre in empresas_nombres:
        try:
            email = f"contact.{nombre.lower().replace(' ', '')}@company.com"
            
            # Verificar si existe
            if db.query(DBUser).filter(DBUser.email == email).first():
                continue
            
            # Crear usuario empresa
            hashed_pwd = hash_password("empresa123")
            nuevo_usuario = DBUser(
                email=email,
                nombre=nombre,
                apellido="Inc",
                tipo=UserRole.empresa,
                hashed_password=hashed_pwd,
                activo=True
            )
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
            
            # Crear perfil empresa
            nueva_empresa = DBEmpresa(
                usuario_id=nuevo_usuario.id,
                nombre=nombre,
                descripcion=fake.text(max_nb_chars=200),
                email_contacto=email,
                telefono=fake.phone_number()[:15],
                ubicacion="Córdoba, Argentina",
                website=f"https://www.{nombre.lower().replace(' ', '')}.com",
                numero_empleados=random.choice(["50-100", "100-250", "250-500", "500+"])
            )
            db.add(nueva_empresa)
            db.commit()
            empresas_creadas += 1
            print(f"✅ Empresa '{nombre}' creada")
            
        except Exception as e:
            print(f"❌ Error creando empresa '{nombre}': {e}")
            db.rollback()
            continue
    
    print(f"\n✅ Se crearon {empresas_creadas} empresas ficticias")
    return empresas_creadas

def crear_oportunidades_ficticias(db):
    """Genera y guarda oportunidades ficticias en la base de datos."""
    
    descripciones_trabajo = [
        "Buscamos un desarrollador apasionado por la tecnología con experiencia en desarrollo web. Trabajarás en proyectos innovadores utilizando las últimas tecnologías del mercado. Ofrecemos un ambiente colaborativo y oportunidades de crecimiento profesional.",
        "Se requiere profesional con habilidades en análisis de datos para unirse a nuestro equipo de Business Intelligence. Participarás en proyectos que impactan directamente nuestro negocio. Brindamos capacitación continua y beneficios competitivos.",
        "Únete a nuestro equipo como especialista en ciberseguridad. Serás responsable de proteger la infraestructura de nuestra empresa. Ofrecemos un entorno desafiante con oportunidades para certificaciones profesionales.",
        "Buscamos desarrollador con experiencia en cloud computing. Trabajarás en la migración y optimización de infraestructura. Ambiente dinámico con acceso a las mejores herramientas del mercado.",
        "Posición disponible para especialista en machine learning. Aplicarás algoritmos avanzados en soluciones empresariales. Colaborarás con un equipo multidisciplinario en proyectos de impacto.",
        "Se busca desarrollador frontend con pasión por UX/UI. Crearás interfaces intuitivas y atractivas para nuestras aplicaciones. Tendrás libertad creativa y oportunidades de innovación.",
        "Oportunidad de práctica profesional en desarrollo backend. Aprenderás mejores prácticas de programación en un equipo experimentado. Mentoring directo y proyecto real durante tu permanencia.",
        "Buscamos técnico en base de datos. Diseñarás y optimizarás sistemas de almacenamiento de datos. Ambiente que valora el aprendizaje continuo y la excelencia técnica.",
        "Se requiere especialista en DevOps para infraestructura en la nube. Automatizarás procesos y mejorarás la eficiencia operativa. Trabajarás con tecnologías de punta en containerización y orquestación.",
        "Posición de analista de sistemas. Evaluarás necesidades de negocio e implementarás soluciones tecnológicas. Ofrecemos capacitación en nuevas tecnologías y un ambiente colaborativo.",
    ]
    
    titulo_templates = [
        "Desarrollador {tipo} Junior",
        "Especialista en {tipo}",
        "Ingeniero de {tipo}",
        "Analyst en {tipo}",
        "Consultor de {tipo}"
    ]
    
    tipos_oportunidad = ["practica", "servicio_social", "empleo"]
    modalidades = ["presencial", "remoto", "hibrido"]
    habilidades_requeridas_lista = [
        ["Python", "SQL"],
        ["React", "Node.js"],
        ["Java", "Spring"],
        ["Python", "Machine Learning"],
        ["Cloud", "Docker"],
        ["SQL", "Power BI"],
        ["Seguridad", "Linux"],
        ["Frontend", "CSS"],
        ["Backend", "APIs"],
        ["DevOps", "Kubernetes"]
    ]
    
    empresas = db.query(DBEmpresa).all()
    if not empresas:
        print("❌ No hay empresas. Crea empresas primero.")
        return 0
    
    oportunidades_creadas = 0
    for empresa in empresas:
        try:
            num_oportunidades = random.randint(2, 4)
            
            for _ in range(num_oportunidades):
                tipo_oportunidad = random.choice(tipos_oportunidad)
                titulo = random.choice(titulo_templates).format(tipo=random.choice(["Python", "React", "Data", "Cloud", "Security"]))
                
                nueva_oportunidad = DBOportunidad(
                    empresa_id=empresa.id,
                    titulo=titulo,
                    descripcion=random.choice(descripciones_trabajo),
                    tipo=tipo_oportunidad,
                    habilidades_requeridas=random.choice(habilidades_requeridas_lista),
                    semestre_minimo=random.randint(3, 6),
                    gpa_minimo=round(random.uniform(7.0, 8.5), 2),
                    ubicacion="Córdoba, Argentina",
                    modalidad=random.choice(modalidades),
                    duracion_meses=random.randint(3, 12) if tipo_oportunidad == "empleo" else random.randint(2, 6),
                    salario=random.randint(15000, 40000) if tipo_oportunidad == "empleo" else None,
                    fecha_cierre=datetime.utcnow() + timedelta(days=random.randint(30, 90)),
                    activa=True
                )
                db.add(nueva_oportunidad)
                oportunidades_creadas += 1
            
            db.commit()
            print(f"✅ {num_oportunidades} oportunidades creadas para '{empresa.nombre}'")
            
        except Exception as e:
            print(f"❌ Error creando oportunidades para '{empresa.nombre}': {e}")
            db.rollback()
            continue
    
    print(f"\n✅ Se crearon {oportunidades_creadas} oportunidades ficticias")
    return oportunidades_creadas

def main():
    print("=" * 60)
    print("SEEDING DE EMPRESAS Y OPORTUNIDADES")
    print("=" * 60)
    
    try:
        db = SessionLocal()
        
        print("\n1️⃣  Creando empresas...")
        crear_empresas_ficticias(db)
        
        print("\n2️⃣  Creando oportunidades...")
        crear_oportunidades_ficticias(db)
        
        print("\n" + "=" * 60)
        print("✅ SEEDING COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante el seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
