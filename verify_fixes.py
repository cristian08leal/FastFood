import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

def run_verification():
    client = APIClient()
    print("Starting verification...")

    # 1. Test User Registration
    print("\nTesting User Registration...")
    register_data = {
        "username": "testuser_verify",
        "email": "testuser_verify@example.com",
        "password": "testpassword123"
    }
    # Clean up if exists
    User.objects.filter(username=register_data["username"]).delete()
    
    response = client.post('/api/auth/register/', register_data)
    if response.status_code == 201:
        print("[OK] User registration successful")
    else:
        print(f"[FAIL] User registration failed: {response.data}")
        return

    # 2. Test Login
    print("\nTesting Login...")
    login_data = {
        "username": "testuser_verify",
        "password": "testpassword123"
    }
    response = client.post('/api/auth/login/', login_data)
    if response.status_code == 200:
        print("[OK] Login successful")
        access_token = response.data['access']
    else:
        print(f"[FAIL] Login failed: {response.data}")
        return

    # 3. Test Product Creation (Unauthorized)
    print("\nTesting Product Creation (Unauthorized)...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    product_data = {
        "nombre": "Test Product",
        "precio": 100.00,
        "categoria": 1  # Assuming category 1 exists or will fail validation differently
    }
    response = client.post('/api/productos/', product_data)
    if response.status_code == 403:
        print("[OK] Unauthorized product creation blocked (403 Forbidden)")
    else:
        print(f"[FAIL] Unexpected status for unauthorized creation: {response.status_code} - {response.data}")

    # 4. Test Product Creation (Admin)
    print("\nTesting Product Creation (Admin)...")
    admin_user, created = User.objects.get_or_create(username="admin_verify", email="admin_verify@example.com")
    if created:
        admin_user.set_password("adminpass123")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
    
    # Get admin token
    response = client.post('/api/auth/login/', {"username": "admin_verify", "password": "adminpass123"})
    admin_token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    
    # Ensure a category exists
    from productos.models import Categoria
    categoria, _ = Categoria.objects.get_or_create(nombre="Test Category")
    
    product_data["categoria"] = categoria.id
    response = client.post('/api/productos/', product_data)
    if response.status_code == 201:
        print("[OK] Admin product creation successful")
    else:
        print(f"[FAIL] Admin product creation failed: {response.data}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
