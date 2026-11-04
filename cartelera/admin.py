from django.contrib import admin

from .models import Genero, Pelicula, Ticket


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'genero', 'precio_pesos', 'en_cartelera']
    list_filter = ['genero', 'en_cartelera']
    search_fields = ['titulo']

    @admin.display(description='Precio')
    def precio_pesos(self, obj):
        return f'${obj.precio:,}'.replace(',', '.')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'pelicula',
        'nombre_comprador',
        'cantidad',
        'fecha_compra',
    ]
    list_filter = ['pelicula']
    search_fields = [
        'codigo',
        'nombre_comprador',
        'correo_comprador',
    ]
    readonly_fields = ['codigo', 'fecha_compra']