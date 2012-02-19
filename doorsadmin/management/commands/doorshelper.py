# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.cron import Helper

class Command(BaseCommand):
    def handle(self, *args, **options):
        Helper()
