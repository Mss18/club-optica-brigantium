from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group


ROLES = ["Cliente", "Dependiente", "Administrador"]


class Command(BaseCommand):
    help = "Instalar y configurar la BD"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando la autoinstalación de la BD")
        call_command("migrate")

        for rol in ROLES:
            grupo, creado = Group.objects.get_or_create(name=rol)            
            if creado:
                self.stdout.write(f"Rol {rol} creado correctamente")
            else:
                self.stdout.write(f"El rol {rol} ya existía")

        self.stdout.write("Autoinstalación de la BD completada")