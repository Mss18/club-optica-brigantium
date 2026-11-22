from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from .models import Usuario


class EstiloBootstrapMixin:
    """Añade las clases de Bootstrap a todos los campos de un formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-check-input"
            else:
                campo.widget.attrs["class"] = "form-control"


class LoginForm(EstiloBootstrapMixin, AuthenticationForm):
    """Formulario de entrada con el estilo de la web."""


class RegistroForm(EstiloBootstrapMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    acepta_privacidad = forms.BooleanField(
        required=True,
        label="He leído y acepto la política de privacidad",
        error_messages={"required": "Debes aceptar la política de privacidad"},
    )

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.fecha_privacidad_aceptada = timezone.now()
        if commit:
            usuario.save()
        return usuario

    class Meta:
        model = Usuario
        fields = ("username", "email")

    def clean_email(self):
        correo = self.cleaned_data["email"]
        if Usuario.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo")
        return correo
