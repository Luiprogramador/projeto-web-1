# check_data.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

def check_data():
    with connection.cursor() as cursor:
        tables = ['user_register', 'event', 'app_eventparticipant', 'certificate']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} registros")

if __name__ == '__main__':
    check_data()