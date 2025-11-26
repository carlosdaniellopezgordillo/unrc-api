"""
Script para agregar columnas faltantes a la tabla estudiantes.
"""
import sqlite3
import os

DB_PATH = "db/database.db"

def migrate():
    """Agrega columnas faltantes a la tabla estudiantes."""
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Obtener columnas existentes
        cursor.execute("PRAGMA table_info(estudiantes)")
        columns = {col[1] for col in cursor.fetchall()}
        
        # Columnas que necesitamos
        required_columns = {
            'cv_path': "TEXT",
            'proyectos': "TEXT",
        }
        
        # Agregar columnas faltantes
        for col_name, col_type in required_columns.items():
            if col_name not in columns:
                print(f"Agregando columna {col_name}...")
                cursor.execute(f"ALTER TABLE estudiantes ADD COLUMN {col_name} {col_type}")
                print(f"✓ Columna {col_name} agregada")
        
        conn.commit()
        print("\n✓ Migración completada exitosamente")
        
        # Mostrar columnas finales
        cursor.execute("PRAGMA table_info(estudiantes)")
        cols = [col[1] for col in cursor.fetchall()]
        print("\nColumnas en tabla estudiantes:")
        for col in cols:
            print(f"  - {col}")
        
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
