from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario de la aplicación. Hereda de AbstractUser, que ya incluye nombre de
    usuario, contraseña cifrada, nombre, apellidos, email y permisos.

    El rol (cliente, dependiente o administrador) se gestiona con los Grupos
    de Django, que se crean con el comando `python manage.py instalar`.
    """

    email = models.EmailField("correo electrónico", unique=True)
    telefono = models.CharField("teléfono", max_length=15, blank=True)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    # Métodos de ayuda para comprobar el rol en vistas y plantillas
    def es_cliente(self):
        return self.groups.filter(name=GRUPO_CLIENTE).exists()

    def es_dependiente(self):
        return self.groups.filter(name=GRUPO_DEPENDIENTE).exists()

    def es_administrador(self):
        return self.is_superuser or self.groups.filter(name=GRUPO_ADMINISTRADOR).exists()


# Nombres de los grupos (roles)
GRUPO_CLIENTE = "Cliente"
GRUPO_DEPENDIENTE = "Dependiente"
GRUPO_ADMINISTRADOR = "Administrador"
ROLES = [GRUPO_CLIENTE, GRUPO_DEPENDIENTE, GRUPO_ADMINISTRADOR]
