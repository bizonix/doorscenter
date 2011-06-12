# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.core import CronDaily

class Command(BaseCommand):
    def handle(self, *args, **options):
        CronDaily()
        self.stdout.write('Done daily\n')
