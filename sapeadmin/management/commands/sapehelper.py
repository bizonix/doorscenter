# coding=utf8
from django.core.management.base import BaseCommand
#from sapeadmin.models import ...

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('done')
