import os
import django
import json
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from usuarios.views import LoginView, VerifyCodeView
from usuarios.models import CodigoVerificacion

User = get_user_model()

# Ensure test user exists
username = 'testuser_2fa'
password = 'TestPassword123!'
email = 'testuser_2fa@example.com'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
except User.DoesNotExist:
    user = User.objects.create_user(username=username, email=email, password=password)

factory = APIRequestFactory()

# Step 1: Login
print("--- Step 1: Login ---")
login_view = LoginView.as_view()
login_data = {'username': username, 'password': password}
request = factory.post('/api/usuarios/login/', login_data, format='json')

# Need to add session middleware support manually for test
from django.contrib.sessions.middleware import SessionMiddleware
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request)
request.session.save()

response = login_view(request)
print(f"Login Status: {response.status_code}")
print(f"Login Response: {response.data}")

if response.status_code != 200 or not response.data.get('requires_2fa'):
    print("Login failed or didn't require 2FA")
    exit(1)

session_id = response.data['session_id']
print(f"Session ID: {session_id}")

# Get the code from DB
codigo_obj = CodigoVerificacion.objects.filter(usuario=user, usado=False).first()
print(f"Code from DB: {codigo_obj.codigo}")

# Step 2: Verify Code
print("\n--- Step 2: Verify Code ---")
verify_view = VerifyCodeView.as_view()
verify_data = {'session_id': session_id, 'codigo': codigo_obj.codigo}
verify_request = factory.post('/api/usuarios/verify-code/', verify_data, format='json')

# Attach the same session
verify_request.session = request.session

verify_response = verify_view(verify_request)
print(f"Verify Status: {verify_response.status_code}")
print(f"Verify Response: {verify_response.data}")

if verify_response.status_code == 200:
    print("2FA Verification Successful!")
else:
    print("2FA Verification Failed!")
