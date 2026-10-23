from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ("username", "email")

    def clean_email(self):
        correo = self.cleaned_data["email"]
        if Usuario.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo")
        return correo
