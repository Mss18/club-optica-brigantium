from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from cuentas.forms import RegistroForm


# Create your views here.
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.groups.add(Group.objects.get(name="Cliente"))
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})


def privacidad(request):
    return render(request, "cuentas/privacidad.html")


@login_required
def baja(request):
    if not request.user.es_cliente():
        messages.error(request, "Solo los clientes pueden darse de baja")
        return redirect("inicio")
    if request.method == "POST":
        usuario = request.user
        logout(request)
        usuario.delete()
        messages.success(request, "Tu cuenta y tus datos se han eliminado")
        return redirect("inicio")
    return render(request, "cuentas/baja.html")


@require_POST
def aceptar_cookies(request):
    """Guarda en una cookie que el usuario ya vio el aviso."""
    respuesta = redirect("inicio")
    respuesta.set_cookie("aviso_cookies", "1", max_age=60 * 60 * 24 * 365, samesite="Lax")
    return respuesta
