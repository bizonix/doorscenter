# coding=utf8
from django.core.management.base import BaseCommand
from sapeadmin.core import CronDaily

class Command(BaseCommand):
    def handle(self, *args, **options):
        CronDaily()
