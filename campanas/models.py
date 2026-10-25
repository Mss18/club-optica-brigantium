import uuid

import segno
from django.conf import settings
from django.db import models


class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, verbose_name="descripción")
    fecha_inicio = models.DateField(verbose_name="fecha de inicio")
    fecha_fin = models.DateField(verbose_name="fecha de fin")
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
    campana = models.ForeignKey(
        Campana, on_delete=models.PROTECT, verbose_name="campaña"
    )
    titulo = models.CharField(max_length=100, verbose_name="título")
    descripcion = models.TextField(blank=True, verbose_name="descripción")
    condiciones = models.TextField(blank=True)
    tipo = models.CharField(choices=TIPOS, max_length=20)
    limite_por_cliente = models.PositiveSmallIntegerField(
        default=1, verbose_name="límite por cliente"
    )

    def __str__(self):
        return self.titulo


class Cupon(models.Model):
    ESTADOS = (
        ("activo", "Activo"),
        ("canjeado", "Canjeado"),
        ("caducado", "Caducado"),
    )
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="código")
    fecha_emision = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de emisión"
    )
    beneficio = models.ForeignKey(Beneficio, on_delete=models.PROTECT)
    fecha_caducidad = models.DateField(verbose_name="fecha de caducidad")
    estado = models.CharField(choices=ESTADOS, max_length=20, default="activo")

    class Meta:
        verbose_name = "cupón"
        verbose_name_plural = "cupones"

    def __str__(self):
        return f"{self.beneficio} - {self.cliente}"

    @property
    def qr(self):
        return segno.make(str(self.codigo)).svg_data_uri(scale=5)


class Canje(models.Model):
    cupon = models.OneToOneField(Cupon, on_delete=models.CASCADE, verbose_name="cupón")
    dependiente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_canje = models.DateTimeField(auto_now_add=True, verbose_name="fecha de canje")

    class Meta:
        verbose_name = "canje"
        verbose_name_plural = "canjes"

    def __str__(self):
        return f"{self.cupon} - {self.fecha_canje}"
