import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from usuarios.views import RegisterView

User = get_user_model()

# Clean up test user if exists
try:
    User.objects.get(username='testuser_reg').delete()
    print("Cleaned up existing test user")
except User.DoesNotExist:
    pass

factory = APIRequestFactory()
view = RegisterView.as_view()

data = {
    'username': 'testuser_reg',
    'password': 'TestPassword123!',
    'email': 'testuser_reg@example.com'
}

request = factory.post('/api/usuarios/register/', data, format='json')
response = view(request)

print(f"Status Code: {response.status_code}")
print(f"Response Data: {response.data}")

if response.status_code == 201:
    print("Registration successful!")
else:
    print("Registration failed!")
