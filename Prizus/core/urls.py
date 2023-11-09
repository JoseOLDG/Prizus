from django import views
from django.urls import path

from .views import index, login, registro, menu, perfumes, update_prices, procesar_imagen_ia

from .views import index, login, login2, registro, menu, admin_dashboard
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views




urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('menu/', menu, name="menu"),
    path('dashboard/', admin_dashboard, name="dashboard"),
    path('producto/<slug>/', perfumes, name="producto"),
    path('procesar_imagen/', procesar_imagen_ia, name="procesar_imagen"),
    path('login2/', login2, name="login2"),
    path('update_prices/<slug>/', update_prices, name='update_prices'),
    path('logout/', views.logout_view, name='logout'),
]