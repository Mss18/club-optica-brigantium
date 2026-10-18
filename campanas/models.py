# Create your models here.

import uuid

from django.conf import settings
from django.db import models


class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "campaña"
        verbose_name_plural = "campañas"

    def __str__(self):
        return self.nombre


class Beneficio(models.Model):
    TIPOS = (
        ("descuento", "Descuento"),
        ("regalo", "Regalo"),
        ("servicio", "Servicio"),
    )
    campana = models.ForeignKey(Campana, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    condiciones = models.TextField(blank=True)
    tipo = models.CharField(choices=TIPOS, max_length=20)
    limite_por_cliente = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.titulo


class Cupon(models.Model):
    ESTADOS = (
        ("activo", "Activo"),
        ("canjeado", "Canjeado"),
        ("caducado", "Caducado"),
    )
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    beneficio = models.ForeignKey(Beneficio, on_delete=models.PROTECT)
    fecha_caducidad = models.DateField()
    estado = models.CharField(choices=ESTADOS, max_length=20, default="activo")

    class Meta:
        verbose_name = "cupón"
        verbose_name_plural = "cupones"

    def __str__(self):
        return f"{self.beneficio} - {self.cliente}"
