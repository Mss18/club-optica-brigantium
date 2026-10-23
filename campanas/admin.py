from django.contrib import admin

from .models import Beneficio, Campana, Canje, Cupon

admin.site.register(Campana)
admin.site.register(Beneficio)
admin.site.register(Cupon)
admin.site.register(Canje)