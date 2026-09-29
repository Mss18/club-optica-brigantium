from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario

# El admin de Django solo se usa como herramienta técnica interna.
# El panel del personal se construye en la app "panel".
admin.site.register(Usuario, UserAdmin)
