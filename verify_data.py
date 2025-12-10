import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from usuarios.models import CustomUser
from productos.models import Producto, Categoria

print("--- VERIFICACIÓN DE DATOS ---")

# Verificar Usuarios
users = CustomUser.objects.all()
print(f"Usuarios encontrados: {users.count()}")
for u in users:
    print(f"- {u.username} (Staff: {u.is_staff}, Superuser: {u.is_superuser})")

# Verificar Categorías
cats = Categoria.objects.all()
print(f"\nCategorías encontradas: {cats.count()}")
for c in cats:
    print(f"- {c.nombre} (ID: {c.id})")

# Verificar Productos
prods = Producto.objects.all()
print(f"\nProductos encontrados: {prods.count()}")
for p in prods:
    print(f"- {p.nombre} (Cat: {p.categoria.nombre}, Disponible: {p.disponible}, Stock: {p.stock})")
