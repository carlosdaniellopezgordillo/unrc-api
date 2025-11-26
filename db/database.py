from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, Boolean, Float, ForeignKey, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import enum

DATABASE_URL = "sqlite:///./db/database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Tabla de asociación para la relación muchos a muchos entre Estudiante y Habilidad
estudiante_habilidad_association = Table('estudiante_habilidad', Base.metadata,
    Column('estudiante_id', Integer, ForeignKey('estudiantes.id')),
    Column('habilidad_id', Integer, ForeignKey('habilidades.id'))
)

class UserRole(str, enum.Enum):
    estudiante = "estudiante"
    empresa = "empresa"
    administrador = "administrador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)  # Nuevo campo para el apellido
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(256))
    tipo = Column(Enum(UserRole))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relación con Estudiante
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    # Relación con Empresa
    empresa = relationship("Empresa", back_populates="usuario", uselist=False)

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    nombre = Column(String, nullable=True, index=True)
    descripcion = Column(String, nullable=True)
    email_contacto = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    ubicacion = Column(String, nullable=True)
    website = Column(String, nullable=True)
    numero_empleados = Column(String, nullable=True)

    # Relación con User
    usuario = relationship("User", back_populates="empresa")
    oportunidades = relationship("Oportunidad", back_populates="empresa")

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    matricula = Column(String, unique=True, index=True, nullable=True)
    semestre = Column(Integer, nullable=True)
    carrera = Column(String, nullable=True)
    gpa = Column(Float, default=0.0, nullable=False)
    habilidades_tecnicas = Column(JSON, default=[], nullable=False)
    habilidades_blandas = Column(JSON, default=[], nullable=False)
    proyectos_lista = Column(JSON, default=[], nullable=False)  # Renombrado de 'proyectos' para evitar conflicto con relationship
    disponibilidad = Column(Boolean, default=True)
    cv_path = Column(String, nullable=True)  # Ruta del CV subido

    # Relación con User
    usuario = relationship("User", back_populates="estudiante")
    experiencias = relationship("Experiencia", back_populates="estudiante")
    proyectos = relationship("Proyecto", back_populates="estudiante")
    habilidades = relationship("Habilidad", secondary=estudiante_habilidad_association, back_populates="estudiantes")

class Habilidad(Base):
    __tablename__ = "habilidades"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    estudiantes = relationship("Estudiante", secondary=estudiante_habilidad_association, back_populates="habilidades")

class Experiencia(Base):
    __tablename__ = "experiencias"
    id = Column(Integer, primary_key=True, index=True)
    puesto = Column(String)
    empresa = Column(String)
    descripcion = Column(String)
    fecha_inicio = Column(String) # Se puede mejorar a Date
    fecha_fin = Column(String, nullable=True) # Puede ser nulo si es el trabajo actual
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    
    estudiante = relationship("Estudiante", back_populates="experiencias")

class Proyecto(Base):
    __tablename__ = "proyectos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    url = Column(String, nullable=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    
    estudiante = relationship("Estudiante", back_populates="proyectos")

class Oportunidad(Base):
    __tablename__ = "oportunidades"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    tipo = Column(String) # 'practica', 'servicio_social', 'empleo'
    habilidades_requeridas = Column(JSON)
    semestre_minimo = Column(Integer)
    gpa_minimo = Column(Float, nullable=True)
    ubicacion = Column(String)
    modalidad = Column(String) # 'presencial', 'remoto', 'hibrido'
    duracion_meses = Column(Integer, nullable=True)
    salario = Column(Float, nullable=True)
    fecha_publicacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_cierre = Column(DateTime, nullable=True)
    activa = Column(Boolean, default=True)

    empresa = relationship("Empresa", back_populates="oportunidades")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
