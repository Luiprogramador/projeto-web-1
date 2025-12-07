import os
import django
import sys
from django.db import transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from app.models import UserRegister 

# Esta é a senha 'senha123' já criptografada.
# Usar ela direto pula o cálculo demorado.
HASH_SENHA_123 = 'pbkdf2_sha256$1000000$JoUFJETr3adnIW0GdRTOxj$LDO9QiuzLtKDPKGKiWcDlTCsB25i8pOyHFeceta6ahk='

def create_users():
    users_data = [
        # --- USUÁRIOS ORIGINAIS (IDs 1 a 5) ---
        {
            'name': 'João Silva', 
            'username': 'joao_organizador', 
            'email': 'joao.organizador@faculdade.edu.br', 
            'phone': '(31) 97777-6666', 
            'institution': 'Faculdade Tecnológica', 
            'user_type': 'Organizador',
            'image': 'usuarios/joao_frango.jpg' 
        },
        {
            'name': 'Ana Costa', 
            'username': 'ana_organizadora', 
            'email': 'ana.organizadora@universidade.edu.br', 
            'phone': '(41) 96666-5555', 
            'institution': 'Universidade Estadual', 
            'user_type': 'Organizador',
            'image': 'usuarios/79bcd3b64a5eab2ff09473f5de649edc.png' 
        },
        {
            'name': 'Maria Silva', 
            'username': 'prof_maria', 
            'email': 'maria.silva@universidade.edu.br', 
            'phone': '(11) 9999-8888', 
            'institution': 'Universidade Federal', 
            'user_type': 'Professor',
            'image': 'usuarios/4c5c7a2d77ce17d9b5d495164e989bb7.png' 
        },
        {
            'name': 'Pedro Santos', 
            'username': 'prof_pedro', 
            'email': 'pedro.santos@instituto.edu.br', 
            'phone': '(21) 98888-7777', 
            'institution': 'Instituto Federal', 
            'user_type': 'Professor',
            'image': 'usuarios/fa8d2b92ecab9a1dc0ac8464f77a98f3.png' 
        },
        {
            'name': 'Lucas Pereira', 
            'username': 'aluno_lucas', 
            'email': 'lucas.pereira@gmail.com', # Corrigido para bater com o SQL
            'phone': '(11) 94444-3333', 
            'institution': 'Universidade Federal', 
            'user_type': 'Estudante',
            'image': 'usuarios/41ed1ff61fc98dec99f78c0f83f29a26.png' 
        },

        # --- NOVOS USUÁRIOS (IDs 6 em diante) ---
        {
            'name': 'Dr. Roberto Almeida', 
            'username': 'prof_roberto', 
            'email': 'roberto.almeida@ciencia.edu.br', 
            'phone': '(61) 93333-2222', 
            'institution': 'UnB - Universidade de Brasília', 
            'user_type': 'Professor',
            'image': None
        },
        {
            'name': 'Fernanda Oliveira', 
            'username': 'nanda_dev', 
            'email': 'fernanda.oliveira@tech.com', 
            'phone': '(11) 98765-4321', 
            'institution': 'USP', 
            'user_type': 'Estudante',
            'image': None
        },
        {
            'name': 'Rafael Souza', 
            'username': 'rafa_eng', 
            'email': 'rafael.souza@engenharia.ufrj.br', 
            'phone': '(21) 91234-5678', 
            'institution': 'UFRJ', 
            'user_type': 'Estudante',
            'image': None
        },
        {
            'name': 'Beatriz Martins', 
            'username': 'bia_dados', 
            'email': 'bia.martins@datascience.com', 
            'phone': '(31) 99876-5432', 
            'institution': 'UFMG', 
            'user_type': 'Estudante',
            'image': None
        },
        {
            'name': 'Gabriel Santos', 
            'username': 'gabriel_gamer', 
            'email': 'gabriel.santos@jogos.edu.br', 
            'phone': '(41) 95555-4444', 
            'institution': 'PUC-PR', 
            'user_type': 'Estudante',
            'image': None
        },
        {
            'name': 'Juliana Costa', 
            'username': 'ju_design', 
            'email': 'juliana.costa@arte.com', 
            'phone': '(51) 97777-1111', 
            'institution': 'UFRGS', 
            'user_type': 'Estudante',
            'image': None
        }
    ]
    
    print("Iniciando criação de usuários (MODO RÁPIDO)...")
    
    for user_data in users_data:
        try:
            with transaction.atomic():
                # Tenta pegar o usuário
                user, created = UserRegister.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'name': user_data['name'],
                        'email': user_data['email'],
                        'phone': user_data['phone'],
                        'institution': user_data['institution'],
                        'user_type': user_data['user_type'],
                        'image': user_data['image'],
                        'password': HASH_SENHA_123 # Define a senha direto na criação
                    }
                )

                if created:
                    print(f"✓ Usuário criado: {user.username}")
                else:
                    # Se já existia, garante que a senha está certa
                    if user.password != HASH_SENHA_123:
                        user.password = HASH_SENHA_123
                        user.save()
                        print(f"↻ Senha corrigida para: {user.username}")
                    else:
                        print(f"⚠ Usuário {user.username} já existe e está OK.")

        except Exception as e:
            print(f"❌ Erro em {user_data['username']}: {e}")

    print("\nConcluído! Pode rodar o SQL de povoação agora.")

if __name__ == '__main__':
    create_users()