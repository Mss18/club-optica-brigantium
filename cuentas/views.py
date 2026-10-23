from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

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