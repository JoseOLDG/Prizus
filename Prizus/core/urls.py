from django import views
from django.urls import path

from .views import index, login, registro, menu, producto

from .views import index, login, login2, registro, menu
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('menu/', menu, name="menu"),

    path('producto/', producto, name="producto"),

    path('login2/', login2, name="login2"),
   

]