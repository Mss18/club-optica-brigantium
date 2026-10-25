from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Beneficio, Campana, Cupon


def inicio(request):
    hoy = timezone.localdate()
    campanas = Campana.objects.filter(
        activa=True,
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy,
    )
    return render(request, "campanas/inicio.html", {"campanas": campanas})


@login_required
@require_POST
def pedir_cupon(request, beneficio_id):
    beneficio = get_object_or_404(Beneficio, id=beneficio_id)
    ya_tiene = Cupon.objects.filter(cliente=request.user, beneficio=beneficio).count()
    if ya_tiene < beneficio.limite_por_cliente:
        Cupon.objects.create(
            cliente=request.user,
            beneficio=beneficio,
            fecha_caducidad=beneficio.campana.fecha_fin,
        )
    return redirect("mis_cupones")

@login_required
def mis_cupones(request):
    cupones = Cupon.objects.filter(cliente=request.user).order_by("-fecha_emision")
    return render(request, "campanas/mis_cupones.html", {"cupones": cupones})