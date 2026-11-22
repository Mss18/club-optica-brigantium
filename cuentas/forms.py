from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    acepta_privacidad = forms.BooleanField(
        required=True,
        label="He leído y acepto la política de privacidad",
        error_messages={"required": "Debes aceptar la política de privacidad"},
    )

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.privacidad_aceptada_el = timezone.now()
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
