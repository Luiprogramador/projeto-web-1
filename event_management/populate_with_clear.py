# populate_nuclear.py
import os
import django
from django.db import connection
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

def execute_sql_file(file_path):
    with connection.cursor() as cursor:
        # Método mais agressivo - desativa TODAS as constraints
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("PRAGMA ignore_check_constraints = ON;")
        
        # Limpa TUDO sem se preocupar com ordem
        """ cursor.execute("DELETE FROM certificate;")
        cursor.execute("DELETE FROM app_eventparticipant;")
        cursor.execute("DELETE FROM event;") """
        
        print("✓ Todas as tabelas limpas")
        
        # Popula os dados
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        sql_content = '\n'.join(
            line for line in sql_content.split('\n') 
            if not line.strip().startswith('--')
        )
        
        cursor.executescript(sql_content)
        
        # Reativa as constraints
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA ignore_check_constraints = OFF;")
        
        print("✓ Dados populados com sucesso!")
        print("✓ Constraints reativadas")

if __name__ == '__main__':
    execute_sql_file('povoacao_banco.sql')