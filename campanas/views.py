from django.shortcuts import render
from django.utils import timezone

from .models import Campana


def inicio(request):
    hoy = timezone.localdate()
    campanas = Campana.objects.filter(
        activa=True,
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy,
    )
    return render(request, "campanas/inicio.html", {"campanas": campanas})