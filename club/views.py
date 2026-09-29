from django.shortcuts import render


def inicio(request):
    """Página pública de presentación del club."""
    return render(request, "club/inicio.html")
