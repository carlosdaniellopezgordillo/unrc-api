import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Añadir raíz al path para importar db
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import Base, engine, Habilidad

DEFAULT_HABILIDADES = [
    'Python','JavaScript','React','Node.js','Django','SQL','PostgreSQL','AWS','Docker','Kubernetes','TensorFlow','pandas',
    'Comunicación','Trabajo en equipo','Liderazgo','Resolución de problemas','Adaptabilidad','Pensamiento crítico'
]

def seed():
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        for name in DEFAULT_HABILIDADES:
            name = name.strip()
            if not name:
                continue
            existing = db.query(Habilidad).filter(Habilidad.nombre == name).first()
            if existing:
                continue
            db.add(Habilidad(nombre=name))
        db.commit()
        print(f"Seeded {len(DEFAULT_HABILIDADES)} habilidades (skipping existentes).")
    except Exception as e:
        print('Error al seedear habilidades:', e)
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed()
