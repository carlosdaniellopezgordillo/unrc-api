#!/usr/bin/env python3
"""
Script para actualizar las descripciones de oportunidades existentes
con textos coherentes.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import SessionLocal, Oportunidad as DBOportunidad

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

def actualizar_descripciones(db):
    """Actualiza todas las descripciones de oportunidades con textos coherentes."""
    import random
    
    oportunidades = db.query(DBOportunidad).all()
    actualizado_count = 0
    
    for oportunidad in oportunidades:
        oportunidad.descripcion = random.choice(descripciones_trabajo)
        actualizado_count += 1
    
    db.commit()
    return actualizado_count

def main():
    print("=" * 80)
    print("ACTUALIZAR DESCRIPCIONES DE OPORTUNIDADES")
    print("=" * 80)
    
    try:
        db = SessionLocal()
        
        print("\n🔄 Actualizando descripciones de oportunidades...")
        count = actualizar_descripciones(db)
        
        print(f"✅ Se actualizaron {count} descripciones de oportunidades")
        print("\n" + "=" * 80)
        print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error durante la actualización: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
