from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Datos del club",
            {"fields": ("telefono", "fecha_nacimiento", "fecha_privacidad_aceptada")},
        ),
    )
    readonly_fields = ("fecha_privacidad_aceptada",)
    list_display = UserAdmin.list_display + ("fecha_privacidad_aceptada",)
