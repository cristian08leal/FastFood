import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from productos.models import Producto, Categoria

print(f"Total Categories: {Categoria.objects.count()}")
for c in Categoria.objects.all():
    print(f" - {c.nombre} (Active: {c.activa})")

print(f"\nTotal Products: {Producto.objects.count()}")
for p in Producto.objects.all():
    print(f" - {p.nombre} (Stock: {p.stock}, Available: {p.disponible}, Category: {p.categoria.nombre})")
