from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import comentario, producto, tiendaOnline, precio, registroHistoricoPrecio


# Register your models here.

admin.site.register(comentario)
admin.site.register(producto)
admin.site.register(tiendaOnline)
admin.site.register(precio)
admin.site.register(registroHistoricoPrecio)