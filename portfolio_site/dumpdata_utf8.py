import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

with open('daten.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', stdout=f)
