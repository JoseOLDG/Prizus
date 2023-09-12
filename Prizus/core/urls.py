from django.urls import path
from .views import index, login, registro, menu, prueba

urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('menu/', menu, name="menu"),
    path('prueba/', prueba, name="prueba"),
]