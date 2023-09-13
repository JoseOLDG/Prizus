from django.urls import path
from .views import index, login, registro, menu

urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('menu/', menu, name="menu"),
]