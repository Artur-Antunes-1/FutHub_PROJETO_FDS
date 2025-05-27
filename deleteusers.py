import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  
django.setup()

from django.contrib.auth.models import User
users = User.objects.all()

for u in users:
    try:
        u.delete()
        print(f"Usuário {u.username} deletado")
    except Exception as e:
        print(f"Erro ao deletar {u.username}: {e}")