#!/usr/bin/env python3
"""
Script para limpiar y recrear usuarios de prueba usando SQLAlchemy
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.modules.auth.services import hash_password

# Crear sesión
db = SessionLocal()

try:
    print("🗑️  Limpiando usuarios de prueba...")
    
    test_emails = [
        'owner@test.com',
        'admin@test.com',
        'mesero@test.com'
    ]
    
    # Eliminar usuarios
    for email in test_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            print(f"  ✓ Eliminado: {email}")
    
    db.commit()
    
    print("\n✅ Usuarios de prueba eliminados correctamente\n")
    
    # Crear nuevos usuarios con roles
    print("🚀 Creando nuevos usuarios con roles...\n")
    
    new_users = [
        {
            "email": "owner@test.com",
            "password": "password123",
            "role": "owner"
        },
        {
            "email": "admin@test.com",
            "password": "password123",
            "role": "admin"
        },
        {
            "email": "mesero@test.com",
            "password": "password123",
            "role": "mesero"
        }
    ]
    
    for user_data in new_users:
        new_user = User(
            email=user_data["email"],
            password=hash_password(user_data["password"]),
            role=user_data["role"]
        )
        db.add(new_user)
        print(f"  ✓ Creado: {user_data['email']} ({user_data['role']})")
    
    db.commit()
    
    print("\n✅ Usuarios de prueba creados correctamente!")
    print("\nDatos de acceso:")
    for user_data in new_users:
        print(f"  Email: {user_data['email']}")
        print(f"  Password: {user_data['password']}")
        print(f"  Rol: {user_data['role']}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
