# Create your models here.


from django.db import models


class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

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
