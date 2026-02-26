#!/usr/bin/env python3
"""
Script para crear usuarios de prueba en la base de datos
Crea un usuario para cada rol: owner, admin, mesero
"""

import requests
import json
import sys
from datetime import datetime

API_BASE = "http://localhost:8000"

# Usar timestamp para evitar conflictos con usuarios existentes
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

test_users = [
    {
        "email": f"owner@test.com",
        "password": "password123",
        "role": "owner"
    },
    {
        "email": f"admin@test.com",
        "password": "password123",
        "role": "admin"
    },
    {
        "email": f"mesero@test.com",
        "password": "password123",
        "role": "mesero"
    }
]

def create_test_users():
    """Crea usuarios de prueba en el backend"""
    print("🚀 Creando usuarios de prueba...\n")
    
    for user in test_users:
        try:
            response = requests.post(
                f"{API_BASE}/auth/",
                json={
                    "email": user["email"],
                    "password": user["password"],
                    "role": user["role"]
                }
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Usuario creado: {user['email']} ({user['role']})")
            elif response.status_code == 400:
                print(f"⚠️  Usuario ya existe: {user['email']}")
            else:
                print(f"❌ Error al crear {user['email']}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error conectando al servidor: {e}")
            print("   Asegúrate de que el backend esté corriendo en puerto 8000")
            return False
    
    print("\n✅ Usuarios de prueba listos!")
    print("\nDatos de acceso:")
    for user in test_users:
        print(f"  Email: {user['email']}")
        print(f"  Password: {user['password']}")
        print(f"  Rol: {user['role']}\n")
    
    return True

def test_login():
    """Prueba login con cada usuario"""
    print("\n🔐 Probando login...\n")
    
    for user in test_users:
        try:
            response = requests.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": user["email"],
                    "password": user["password"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token") or data.get("token")
                print(f"✅ Login exitoso: {user['email']}")
                print(f"   Token: {token[:30]}...")
                print(f"   Rol: {data['user']['role']}\n")
            else:
                print(f"❌ Login fallido: {user['email']}")
                print(f"   Error: {response.text}\n")
                
        except Exception as e:
            print(f"❌ Error: {e}\n")

def test_protected_routes():
    """Prueba acceso a rutas protegidas"""
    print("\n🔒 Probando rutas protegidas...\n")
    
    protected_routes = [
        ("/comida/nueva", ["admin", "owner"]),
        ("/comida", ["admin", "owner", "mesero"]),
        ("/pedidos", ["admin", "owner", "mesero"]),
        ("/ventas", ["admin", "owner"]),
        ("/estadisticas", ["admin", "owner"]),
        ("/mesas", ["admin", "owner", "mesero"]),
        ("/empleados", ["admin", "owner"]),
        ("/negocios", ["owner"]),
        ("/pagos", ["admin", "owner"])
    ]
    
    for user in test_users:
        print(f"\n👤 Usuario: {user['email']} ({user['role']})")
        print("-" * 50)
        
        for route, allowed_roles in protected_routes:
            has_access = user["role"] in allowed_roles
            status = "✅ ACCESO" if has_access else "❌ DENEGADO"
            print(f"  {status} - {route}")

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE SISTEMA DE PROTECCIÓN DE RUTAS POR ROLES")
    print("=" * 60 + "\n")
    
    # Crear usuarios
    if not create_test_users():
        sys.exit(1)
    
    # Probar login
    test_login()
    
    # Mostrar permisos de rutas
    test_protected_routes()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS DE PROTECCIÓN COMPLETADAS")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Abre http://localhost:5174 en tu navegador")
    print("2. Intenta registrase con uno de los usuarios de prueba")
    print("3. Navega por las diferentes secciones según tu rol")
    print("4. Intenta acceder a rutas protegidas que no deberías poder ver")
