import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from productos.views import ProductoViewSet
from productos.models import Producto

def check_products_api():
    print("Checking products in database...")
    count = Producto.objects.count()
    print(f"Total products: {count}")
    
    if count > 0:
        print("First 5 products:")
        for p in Producto.objects.all()[:5]:
            print(f"- {p.nombre} (Disponible: {p.disponible}, Stock: {p.stock}, Categoria: {p.categoria})")

    print("\nChecking API response...")
    factory = APIRequestFactory()
    request = factory.get('/api/productos/')
    view = ProductoViewSet.as_view({'get': 'list'})
    response = view(request)
    
    print(f"Status Code: {response.status_code}")
    print(f"Data: {response.data}")

if __name__ == "__main__":
    check_products_api()
