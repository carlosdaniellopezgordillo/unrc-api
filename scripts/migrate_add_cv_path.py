"""
Script para agregar la columna cv_path a la tabla estudiantes si no existe.
Ejecutar: python scripts/migrate_add_cv_path.py
"""
import sqlite3
import os

DB_PATH = "db/database.db"

def migrate():
    """Agrega la columna cv_path a la tabla estudiantes si no existe."""
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(estudiantes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'cv_path' in columns:
            print("La columna cv_path ya existe en la tabla estudiantes")
            return True
        
        # Agregar la columna si no existe
        print("Agregando columna cv_path a la tabla estudiantes...")
        cursor.execute("ALTER TABLE estudiantes ADD COLUMN cv_path TEXT")
        conn.commit()
        print("✓ Columna cv_path agregada exitosamente")
        return True
        
    except Exception as e:
        print(f"✗ Error durante la migración: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = migrate()
    exit(0 if success else 1)
