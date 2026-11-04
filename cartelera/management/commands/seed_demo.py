from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from cartelera.models import Genero, Pelicula, Ticket


class Command(BaseCommand):
    help = 'Carga usuarios, películas, imágenes y tickets de demostración.'

    @transaction.atomic
    def handle(self, *args, **options):
        user_model = get_user_model()

        admin, _ = user_model.objects.get_or_create(username='admin')
        admin.set_password('Inacap.2026')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        programacion, _ = user_model.objects.get_or_create(
            username='programacion',
        )
        programacion.set_password('Inacap.2026')
        programacion.is_staff = True
        programacion.save()

        grupo, _ = Group.objects.get_or_create(name='Programación')
        permisos = Permission.objects.filter(
            content_type__app_label='cartelera',
            codename__in=[
                'view_genero',
                'add_genero',
                'change_genero',
                'view_pelicula',
                'add_pelicula',
                'change_pelicula',
                'view_ticket',
            ],
        )
        grupo.permissions.set(permisos)
        programacion.groups.set([grupo])

        generos = {
            nombre: Genero.objects.get_or_create(nombre=nombre)[0]
            for nombre in [
                'Acción',
                'Comedia',
                'Ciencia ficción',
            ]
        }

        peliculas = [
            ('Horizonte rojo', 'Acción', True, 4500),
            ('Risas de domingo', 'Comedia', True, 4000),
            ('Órbita final', 'Ciencia ficción', True, 5500),
            ('La última misión', 'Acción', True, 5000),
            ('Café para dos', 'Comedia', True, 3500),
            ('Planeta distante', 'Ciencia ficción', False, 6000),
        ]

        registros = []

        for titulo, nombre_genero, en_cartelera, precio in peliculas:
            pelicula, _ = Pelicula.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'genero': generos[nombre_genero],
                    'sinopsis': (
                        f'Una historia de {nombre_genero.lower()} '
                        'para disfrutar en el cine.'
                    ),
                    'duracion': 110,
                    'fecha_estreno': '2026-01-15',
                    'precio': precio,
                    'en_cartelera': en_cartelera,
                },
            )

            if not pelicula.afiche:
                pelicula.afiche.save(
                    f'{pelicula.pk}.png',
                    ContentFile(self.crear_afiche(titulo)),
                    save=True,
                )

            registros.append(pelicula)

        if not Ticket.objects.exists():
            compras = [
                ('Ana Pérez', 'ana@example.com', 2, registros[0]),
                ('Bruno Soto', 'bruno@example.com', 1, registros[1]),
                ('Carla Díaz', 'carla@example.com', 3, registros[2]),
                ('Diego Rojas', 'diego@example.com', 2, registros[3]),
            ]

            for nombre, correo, cantidad, pelicula in compras:
                Ticket.objects.create(
                    pelicula=pelicula,
                    nombre_comprador=nombre,
                    correo_comprador=correo,
                    cantidad=cantidad,
                )

        self.stdout.write(
            self.style.SUCCESS('Datos de demostración cargados.')
        )

    @staticmethod
    def crear_afiche(titulo):
        imagen = Image.new('RGB', (600, 900), '#172554')
        dibujo = ImageDraw.Draw(imagen)
        dibujo.text((40, 420), titulo, fill='white')

        archivo = BytesIO()
        imagen.save(archivo, format='PNG')
        return archivo.getvalue()