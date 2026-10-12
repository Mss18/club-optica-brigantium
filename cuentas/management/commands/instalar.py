from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Instalar y configurar la BD"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando la autoinstalación de la BD")
        call_command("migrate")
        self.stdout.write("Autoinstalación de la BD completada")