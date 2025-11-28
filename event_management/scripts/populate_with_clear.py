import os
import django
from django.db import connection
import sys

# Diretório onde está este script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

def execute_sql_file(file_path):
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("PRAGMA ignore_check_constraints = ON;")

        cursor.execute("DELETE FROM certificate;")
        cursor.execute("DELETE FROM app_eventparticipant;")
        cursor.execute("DELETE FROM event;")

        print("✓ Todas as tabelas limpas")

        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()

        sql_content = '\n'.join(
            line for line in sql_content.split('\n')
            if not line.strip().startswith('--')
        )

        cursor.executescript(sql_content)

        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA ignore_check_constraints = OFF;")

        print("✓ Dados populados com sucesso!")
        print("✓ Constraints reativadas")

if __name__ == '__main__':
    sql_file = os.path.join(SCRIPT_DIR, 'povoacao_banco.sql')
    execute_sql_file(sql_file)
