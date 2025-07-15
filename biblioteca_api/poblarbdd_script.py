import os
import django
from django.core.management import call_command

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_api.settings')
django.setup()

def poblar_desde_fixture():
    try:
        fixture_path = 'datos.json'  
        call_command('loaddata', fixture_path)
        print("Base de datos poblada desde fixture JSON.")
    except Exception as e:
        print(f"Error al cargar datos: {e}")

if __name__ == '__main__':
    poblar_desde_fixture()
