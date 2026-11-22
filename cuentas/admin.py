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
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "telefono")}),
    )
    readonly_fields = ("fecha_privacidad_aceptada",)
    list_display = (
        "username",
        "email",
        "telefono",
        "is_active",
        "fecha_privacidad_aceptada",
    )
    list_filter = ("groups", "is_active")
    search_fields = ("username", "email", "telefono")
    ordering = ("username",)
