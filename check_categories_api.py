import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from productos.views import CategoriaViewSet
from productos.models import Categoria

def check_categories_api():
    print("Checking categories in database...")
    count = Categoria.objects.count()
    print(f"Total categories: {count}")
    
    if count > 0:
        print("First 5 categories:")
        for c in Categoria.objects.all()[:5]:
            print(f"- {c.nombre} (Activa: {c.activa})")

    print("\nChecking API response...")
    factory = APIRequestFactory()
    request = factory.get('/api/categorias/')
    view = CategoriaViewSet.as_view({'get': 'list'})
    response = view(request)
    
    print(f"Status Code: {response.status_code}")
    print(f"Data: {response.data}")

if __name__ == "__main__":
    check_categories_api()
