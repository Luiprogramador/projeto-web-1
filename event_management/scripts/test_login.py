# test_login.py
import os
import django
from django.contrib.auth import authenticate
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from app.models import UserRegister

def test_login():
    username = "joao_organizador"
    password = "senha123"
    
    # Tenta autenticar
    user = authenticate(username=username, password=password)
    
    if user is not None:
        print(f"✓ Login bem-sucedido para: {username}")
        print(f"  Tipo de usuário: {user.user_type}")
    else:
        print(f"✗ Falha no login para: {username}")
        print("  Verifique se a senha está com hash válido")

if __name__ == '__main__':
    test_login()