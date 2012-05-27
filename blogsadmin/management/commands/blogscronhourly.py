# coding=utf8
from django.core.management.base import BaseCommand
from blogsadmin.cron import CronHourly

class Command(BaseCommand):
    def handle(self, *args, **options):
        CronHourly()
