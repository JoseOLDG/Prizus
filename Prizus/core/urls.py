from django import views
from django.urls import path

from .views import index, login, registro, menu, perfumes, update_prices, procesar_imagen_ia

from .views import index, login, login2, registro, menu, admin_dashboard, admin_perfumes, admin_perfumes_detail ,admin_precios, admin_precios_actualizar ,admin_tendencias, new_prices, generar_excel
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views




urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('menu/', menu, name="menu"),
    path('dashboard/', admin_dashboard, name="dashboard"),
    path('dashboard/perfumes', admin_perfumes, name="perfumes"),
    path('dashboard/<slug>/', admin_perfumes_detail, name="perfumes_detail"),
    path('dashboard/precios', admin_precios, name="precios"),
    path('dashboard/precios/<nombre>', admin_precios_actualizar, name="actualizar_precios"),
    path('dashboard/precios/update/<id>', update_prices, name='update_prices'),
    path('dashboard/precios/create/<id>', new_prices, name='new_prices'),
    path('dashboard/tendencias', admin_tendencias, name="tendencias"),
    path('dashboard/tendencias/report', generar_excel, name='report'),
    path('producto/<slug>/', perfumes, name="producto"),
    path('procesar_imagen/', procesar_imagen_ia, name="procesar_imagen"),
    path('login2/', login2, name="login2"),
    path('logout/', views.logout_view, name='logout'),
]