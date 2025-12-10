import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from rest_framework.test import APIClient
from usuarios.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

# Get admin user
admin = CustomUser.objects.filter(is_staff=True, is_superuser=True).first()
if not admin:
    print("❌ No admin user found!")
    exit(1)

print(f"[OK] Admin user found: {admin.username}")
print(f"  - Email: {admin.email}")
print(f"  - Is staff: {admin.is_staff}")
print(f"  - Is superuser: {admin.is_superuser}")

# Generate JWT token
refresh = RefreshToken.for_user(admin)
access_token = str(refresh.access_token)

print(f"\n[OK] Generated access token: {access_token[:50]}...")

# Create API client
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

# Test admin productos endpoint
print("\n" + "="*60)
print("Testing /api/admin/productos/ endpoint")
print("="*60)

response = client.get('/api/admin/productos/')
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    print(f"[OK] Success! Retrieved {len(response.data.get('results', []))} products")
    if response.data.get('results'):
        print(f"\nFirst product:")
        first_product = response.data['results'][0]
        for key, value in first_product.items():
            print(f"  {key}: {value}")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response data: {response.data}")
