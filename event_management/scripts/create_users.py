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
    {
        'name': 'João Silva', 
        'username': 'joao_organizador', 
        'email': 'joao.organizador@faculdade.edu.br', 
        'password': 'senha123', 
        'phone': '(31) 97777-6666', 
        'institution': 'Faculdade Tecnológica', 
        'user_type': 'Organizador',
        'image': 'usuarios/joao_frango.jpg' 
    },
    {
        'name': 'Ana Costa', 
        'username': 'ana_organizadora', 
        'email': 'ana.organizadora@universidade.edu.br', 
        'password': 'senha123', 
        'phone': '(41) 96666-5555', 
        'institution': 'Universidade Estadual', 
        'user_type': 'Organizador',
        'image': 'usuarios/79bcd3b64a5eab2ff09473f5de649edc.png' 
    },
    
    # Professores  
    {
        'name': 'Maria Silva', 
        'username': 'prof_maria', 
        'email': 'maria.silva@universidade.edu.br', 
        'password': 'senha123', 
        'phone': '(11) 9999-8888', 
        'institution': 'Universidade Federal', 
        'user_type': 'Professor',
        'image': 'usuarios/4c5c7a2d77ce17d9b5d495164e989bb7.png' 
    },
    {
        'name': 'Pedro Santos', 
        'username': 'prof_pedro', 
        'email': 'pedro.santos@instituto.edu.br', 
        'password': 'senha123', 
        'phone': '(21) 98888-7777', 
        'institution': 'Instituto Federal', 
        'user_type': 'Professor',
        'image': 'usuarios/fa8d2b92ecab9a1dc0ac8464f77a98f3.png' 
    },
    
    # Estudantes
    {
        'name': 'Lucas Pereira', 
        'username': 'aluno_lucas', 
        'email': 'lucas.pereira@gmail.com', 
        'password': 'senha123', 
        'phone': '(11) 94444-3333', 
        'institution': 'Universidade Federal', 
        'user_type': 'Estudante',
        'image': 'usuarios/41ed1ff61fc98dec99f78c0f83f29a26.png' 
    },
]
    
    for user_data in users_data:
        # Cria o usuário usando o modelo (Django fará o hash automaticamente)
        user = UserRegister.objects.create(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            phone=user_data['phone'],
            institution=user_data['institution'],
            user_type=user_data['user_type'],
            image=user_data['image']
        )
        # Define a senha (Django faz o hash automaticamente)
        user.set_password(user_data['password'])
        user.save()
        print(f"✓ Usuário criado: {user.username}")

if __name__ == '__main__':
    create_users()