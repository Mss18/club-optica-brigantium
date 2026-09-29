"""
Comando de autoinstalación:  python manage.py instalar

1. Crea la base de datos en MySQL si no existe.
2. Aplica las migraciones (crea las tablas).
3. Crea los grupos de usuarios (roles).
4. Crea el primer administrador si no hay ninguno.
"""
import getpass

import MySQLdb
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cuentas.models import GRUPO_ADMINISTRADOR, ROLES


class Command(BaseCommand):
    help = "Instala y configura la base de datos del Club Óptica Brigantium"

    def handle(self, *args, **options):
        self.crear_base_de_datos()
        self.stdout.write("Aplicando migraciones...")
        call_command("migrate", interactive=False)
        self.crear_roles()
        self.crear_administrador()
        self.stdout.write(self.style.SUCCESS("Instalación completada."))

    def crear_base_de_datos(self):
        """Se conecta a MySQL sin elegir base de datos y la crea si hace falta."""
        db = settings.DATABASES["default"]
        conexion = MySQLdb.connect(
            host=db["HOST"], port=int(db["PORT"]), user=db["USER"], passwd=db["PASSWORD"]
        )
        cursor = conexion.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db['NAME']}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conexion.close()
        self.stdout.write(f"Base de datos '{db['NAME']}' lista.")

    def crear_roles(self):
        for nombre in ROLES:
            _, creado = Group.objects.get_or_create(name=nombre)
            if creado:
                self.stdout.write(f"Rol creado: {nombre}")
        # Los permisos de cada rol se asignarán aquí cuando existan los modelos.

    def crear_administrador(self):
        Usuario = get_user_model()
        if Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write("Ya existe un administrador.")
            return
        self.stdout.write("Creación del primer administrador:")
        username = input("  Nombre de usuario: ")
        email = input("  Correo electrónico: ")
        password = getpass.getpass("  Contraseña: ")
        admin = Usuario.objects.create_superuser(username=username, email=email, password=password)
        admin.groups.add(Group.objects.get(name=GRUPO_ADMINISTRADOR))
        self.stdout.write(self.style.SUCCESS(f"Administrador '{username}' creado."))
