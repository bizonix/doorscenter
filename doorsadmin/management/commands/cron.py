# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.core import Cron

class Command(BaseCommand):
    def handle(self, *args, **options):
        Cron()
        self.stdout.write('Done\n')
