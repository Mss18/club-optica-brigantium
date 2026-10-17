from getpass import getpass

import MySQLdb
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cuentas.models import Usuario

ROLES = ["Cliente", "Dependiente", "Administrador"]


class Command(BaseCommand):
    help = "Instalar y configurar la BD"

    def crear_base_datos(self):
        bd = settings.DATABASES["default"]
        conexion = MySQLdb.connect(
            host=bd["HOST"],
            user=bd["USER"],
            passwd=bd["PASSWORD"],
            port=int(bd["PORT"]),
        )
        cursor = conexion.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{bd['NAME']}` CHARACTER SET utf8mb4"
        )
        conexion.close()

    def handle(self):
        self.stdout.write("Iniciando la autoinstalación de la BD")
        self.crear_base_datos()
        call_command("migrate")

        for rol in ROLES:
            _, creado = Group.objects.get_or_create(name=rol)
            if creado:
                self.stdout.write(f"Rol {rol} creado correctamente")
            else:
                self.stdout.write(f"El rol {rol} ya existía")

        if Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write("Ya existe un superusuario")
        else:
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
                self.stdout.write(
                    f"Administrador {nombre_usuario} creado correctamente"
                )

        self.stdout.write("Autoinstalación de la BD completada")
