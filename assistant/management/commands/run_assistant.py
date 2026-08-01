from django.core.management.base import BaseCommand
from app import run_cli


class Command(BaseCommand):
    help = 'Runs the Shifra Voice Assistant CLI loop inside Django context'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Shifra Assistant with Django configuration...'))
        run_cli()
