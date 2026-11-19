import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Beneficio, Campana, Canje, Cupon

logger = logging.getLogger("canjes")


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
    if not beneficio.campana.esta_vigente():
        messages.error(request, "Esta campaña no está disponible")
        return redirect("inicio")               
    ya_tiene = Cupon.objects.filter(cliente=request.user, beneficio=beneficio).count()
    if ya_tiene < beneficio.limite_por_cliente:
        Cupon.objects.create(
            cliente=request.user,
            beneficio=beneficio,
            fecha_caducidad=beneficio.campana.fecha_fin,
        )
    else:
        messages.error(request, "Ya tienes el máximo de cupones de este beneficio")
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
            with transaction.atomic():
                cupon = Cupon.objects.select_for_update().get(codigo=codigo)
                if cupon.estado != "activo":
                    messages.error(request, "Este cupón ya no está activo")
                    logger.warning(
                        "RECHAZADO codigo=%r motivo=no_activo dependiente=%s",
                        codigo,
                        request.user.username,
                    )
                elif cupon.fecha_caducidad < timezone.localdate():
                    messages.error(request, "Este cupón ha caducado")
                    logger.warning(
                        "RECHAZADO codigo=%r motivo=caducado dependiente=%s",
                        codigo,
                        request.user.username,
                    )
                else:
                    Canje.objects.create(cupon=cupon, dependiente=request.user)
                    cupon.estado = "canjeado"
                    cupon.save()
                    transaction.on_commit(
                        lambda: logger.info(
                            "CANJE cupon=%s dependiente=%s",
                            cupon.codigo,
                            request.user.username,
                        )
                    )
                    messages.success(request, f"Cupón canjeado: {cupon.beneficio}")
        except (Cupon.DoesNotExist, ValidationError):
            messages.error(request, "El código no existe")
            logger.warning(
                "RECHAZADO codigo=%r motivo=codigo_inexistente dependiente=%s",
                codigo,
                request.user.username,
            )
        except IntegrityError:
            messages.error(request, "Este cupón ya no está activo")
            logger.warning(
                "RECHAZADO codigo=%r motivo=doble_canje dependiente=%s",
                codigo,
                request.user.username,
            )
    return render(request, "campanas/canjear.html")
