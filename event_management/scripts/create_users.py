# create_valid_users.py
import os
import django
from django.contrib.auth.hashers import make_password
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from app.models import UserRegister  # Ajuste para o nome do seu modelo

def create_users():
    users_data = [
        # Organizadores
        {'name': 'João Silva', 'username': 'joao_organizador', 'email': 'joao.organizador@faculdade.edu.br', 'password': 'senha123', 'phone': '(31) 97777-6666', 'institution': 'Faculdade Tecnológica', 'user_type': 'Organizador'},
        {'name': 'Ana Costa', 'username': 'ana_organizadora', 'email': 'ana.organizadora@universidade.edu.br', 'password': 'senha123', 'phone': '(41) 96666-5555', 'institution': 'Universidade Estadual', 'user_type': 'Organizador'},
        
        # Professores  
        {'name': 'Maria Silva', 'username': 'prof_maria', 'email': 'maria.silva@universidade.edu.br', 'password': 'senha123', 'phone': '(11) 9999-8888', 'institution': 'Universidade Federal', 'user_type': 'Professor'},
        {'name': 'Pedro Santos', 'username': 'prof_pedro', 'email': 'pedro.santos@instituto.edu.br', 'password': 'senha123', 'phone': '(21) 98888-7777', 'institution': 'Instituto Federal', 'user_type': 'Professor'},
        
        # Estudantes
        {'name': 'Lucas Pereira', 'username': 'aluno_lucas', 'email': 'lucas.pereira@gmail.com', 'password': 'senha123', 'phone': '(11) 94444-3333', 'institution': 'Universidade Federal', 'user_type': 'Estudante'},
    ]
    
    for user_data in users_data:
        # Cria o usuário usando o modelo (Django fará o hash automaticamente)
        user = UserRegister.objects.create(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            phone=user_data['phone'],
            institution=user_data['institution'],
            user_type=user_data['user_type']
        )
        # Define a senha (Django faz o hash automaticamente)
        user.set_password(user_data['password'])
        user.save()
        print(f"✓ Usuário criado: {user.username}")

if __name__ == '__main__':
    create_users()