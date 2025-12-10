# Test 2FA Login Flow
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from rest_framework.test import APIClient
from usuarios.models import CustomUser
import json

# Create API client
client = APIClient()

print("\n" + "="*60)
print("Testing 2FA Login Flow")
print("="*60)

# Get or create test user
test_username = "testuser2fa"
test_password = "testpass123"

user, created = CustomUser.objects.get_or_create(
    username=test_username,
    defaults={
        'email': 'testuser2fa@example.com'
    }
)
if created or not user.check_password(test_password):
    user.set_password(test_password)
    user.save()
    print(f"\n[OK] Test user created/updated: {test_username}")
else:
    print(f"\n[OK] Test user exists: {test_username}")

# Step 1: Login with credentials
print("\n--- Step 1: Login with credentials ---")
response = client.post('/api/usuarios/login/', {
    'username': test_username,
    'password': test_password
}, format='json')

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.data, indent=2)}")

if response.status_code == 200 and response.data.get('requires_2fa'):
    session_id = response.data.get('session_id')
    debug_code = response.data.get('debug_code')
    
    print(f"\n[OK] 2FA required")
    print(f"Session ID: {session_id}")
    print(f"Debug Code: {debug_code}")
    
    # Step 2: Verify code
    print("\n--- Step 2: Verify code ---")
    response2 = client.post('/api/usuarios/verify-code/', {
        'session_id': session_id,
        'codigo': debug_code
    }, format='json')
    
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {json.dumps(response2.data, indent=2)}")
    
    if response2.status_code == 200:
        print("\n[OK] 2FA verification successful!")
        print(f"Access token received: {response2.data.get('access')[:50]}...")
    else:
        print("\n[ERROR] 2FA verification failed!")
else:
    print("\n[ERROR] Login failed or 2FA not required!")

print("\n" + "="*60)
