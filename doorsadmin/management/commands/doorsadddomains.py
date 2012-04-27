# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.manual import AddDomains

class Command(BaseCommand):
    def handle(self, *args, **options):
        AddDomains()
