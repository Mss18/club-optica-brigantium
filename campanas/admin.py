from django.contrib import admin

from .models import Beneficio, Campana, Cupon

admin.site.register(Campana)
admin.site.register(Beneficio)
admin.site.register(Cupon)
