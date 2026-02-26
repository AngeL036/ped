#!/usr/bin/env python3
"""
Script para limpiar usuarios de prueba de la BD
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'pedidosapp'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    print("🗑️  Limpiando usuarios de prueba...")
    
    # Eliminar usuarios de prueba
    test_emails = [
        'owner@test.com',
        'admin@test.com',
        'mesero@test.com'
    ]
    
    for email in test_emails:
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        print(f"  ✓ Eliminado: {email}")
    
    connection.commit()
    
    print("\n✅ Usuarios de prueba eliminados correctamente")
    print("\nAhora puedes ejecutar test_role_protection.py para crear nuevos usuarios")
    
    cursor.close()
    connection.close()
    
except Error as err:
    print(f"❌ Error: {err}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
