from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Instalar y configurar la BD"

    def handle(self, *args, **options):
        self.stdout.write("Hola")