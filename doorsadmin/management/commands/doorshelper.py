# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.models import Net

class Command(BaseCommand):
    def handle(self, *args, **options):
        for net in Net.objects.filter(active=True).order_by('pk').all():
            net.BuildNet()
