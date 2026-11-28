from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mass_mail
from django.utils import timezone

from campanas.models import Cupon

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

    actions = ["enviar_cupones_por_correo"]

    @admin.action(description="Enviar por correo sus cupones activos")
    def enviar_cupones_por_correo(self, request, queryset):
        """Manda a cada usuario seleccionado la lista de sus cupones activos."""
        mensajes = []
        for usuario in queryset:
            # Solo cupones activos y que no hayan caducado todavía.
            cupones = Cupon.objects.filter(
                cliente=usuario,
                estado="activo",
                fecha_caducidad__gte=timezone.localdate(),
            ).select_related("beneficio")
            if not usuario.email or not cupones:
                continue
            lineas = [
                f"- {c.beneficio.titulo}: {c.codigo} (caduca el {c.fecha_caducidad:%d/%m/%Y})"
                for c in cupones
            ]
            cuerpo = (
                f"Hola, {usuario.username}:\n\n"
                "Estos son tus cupones activos del Club Óptica Brigantium:\n\n"
                + "\n".join(lineas)
                + "\n\nEnséñalos en la tienda.\n"
            )
            mensajes.append(
                (
                    "Tus cupones del Club Óptica Brigantium",
                    cuerpo,
                    None,
                    [usuario.email],
                )
            )
        # Una sola conexión al servidor de correo para todos los mensajes.
        send_mass_mail(mensajes)
        aviso = f"Correos enviados: {len(mensajes)}"
        if settings.EMAIL_BACKEND.endswith("console.EmailBackend"):
            aviso += (
                " (modo prueba: se muestran en la consola del servidor, no se envían)"
            )
        self.message_user(request, aviso)
