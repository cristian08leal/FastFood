import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from productos.models import Categoria

try:
    categoria = Categoria.objects.get(nombre="Categoría de prueba")
    print(f"Deleting category: {categoria.nombre} (ID: {categoria.id})")
    categoria.delete()
    print("Category deleted successfully.")
except Categoria.DoesNotExist:
    print("Category 'Categoría de prueba' not found.")
except Exception as e:
    print(f"Error deleting category: {e}")
