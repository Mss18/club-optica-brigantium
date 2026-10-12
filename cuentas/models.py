from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='correo electrónico')
