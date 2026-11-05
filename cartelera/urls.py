from django.urls import path

from . import views

app_name = 'cartelera'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('pelicula/<int:pk>/', views.detalle, name='detalle'),
]