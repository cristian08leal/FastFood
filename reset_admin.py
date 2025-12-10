import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
password = '2708'
email = 'admin@example.com'

try:
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.rol = 'admin'
        user.save()
        print(f"User '{username}' updated successfully. Password set to '{password}'.")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"User '{username}' created successfully with password '{password}'.")
except Exception as e:
    print(f"Error: {e}")
