from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group
from cuentas.models import Usuario
from getpass import getpass


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

        nombre_usuario = input("Nombre de usuario: ")

        if Usuario.objects.filter(username=nombre_usuario).exists():
            self.stdout.write(
                f"El usuario {nombre_usuario} ya había sido registrado anteriormente"
            )
        else:
            correo = input("Indica un correo: ")
            clave = getpass("Contraseña: ")

            administrador = Usuario.objects.create_superuser(
                username=nombre_usuario, email=correo, password=clave
            )
            administrador.groups.add(Group.objects.get(name="Administrador"))
            self.stdout.write(f"Administrador {nombre_usuario} creado correctamente")

        self.stdout.write("Autoinstalación de la BD completada")
