from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from .models import Beneficio, Campana, Canje, Cupon


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
    if not request.user.es_cliente():
        messages.error(request, "Solo los clientes pueden pedir cupones")
        return redirect("inicio")
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


def es_dependiente(usuario):
    return usuario.groups.filter(name="Dependiente").exists()


@login_required
@user_passes_test(es_dependiente)
def canjear(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo", "").strip()
        try:
            cupon = Cupon.objects.get(codigo=codigo)
        except (Cupon.DoesNotExist, ValidationError):
            messages.error(request, "El código no existe")
        else:
            if cupon.estado != "activo":
                messages.error(request, "Este cupón ya no está activo")
            elif cupon.fecha_caducidad < timezone.localdate():
                messages.error(request, "Este cupón ha caducado")
            else:
                Canje.objects.create(cupon=cupon, dependiente=request.user)
                cupon.estado = "canjeado"
                cupon.save()
                messages.success(request, f"Cupón canjeado: {cupon.beneficio}")
    return render(request, "campanas/canjear.html")
