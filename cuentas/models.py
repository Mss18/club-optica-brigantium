from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="correo electrónico")

    def es_cliente(self):
        return self.groups.filter(name="Cliente").exists()
