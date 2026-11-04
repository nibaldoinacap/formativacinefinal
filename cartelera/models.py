import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'género'
        verbose_name_plural = 'géneros'

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    genero = models.ForeignKey(
        Genero,
        on_delete=models.CASCADE,
        related_name='peliculas',
    )
    titulo = models.CharField(max_length=200)
    sinopsis = models.TextField()
    duracion = models.PositiveIntegerField(
        help_text='Duración en minutos',
    )
    fecha_estreno = models.DateField()
    afiche = models.ImageField(upload_to='afiches/')
    precio = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    en_cartelera = models.BooleanField(default=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'película'
        verbose_name_plural = 'películas'

    def __str__(self):
        return self.titulo


class Ticket(models.Model):
    codigo = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    pelicula = models.ForeignKey(
        Pelicula,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    nombre_comprador = models.CharField(max_length=150)
    correo_comprador = models.EmailField()
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    fecha_compra = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    def __str__(self):
        return f'{self.codigo} - {self.pelicula}'