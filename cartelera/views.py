from django.shortcuts import get_object_or_404, render

from .models import Genero, Pelicula


def inicio(request):
    peliculas = Pelicula.objects.filter(
        en_cartelera=True,
    ).select_related('genero')

    busqueda = request.GET.get('q', '').strip()
    genero_id = request.GET.get('genero', '')

    if busqueda:
        peliculas = peliculas.filter(titulo__icontains=busqueda)

    if genero_id:
        peliculas = peliculas.filter(genero_id=genero_id)

    return render(
        request,
        'cartelera/inicio.html',
        {
            'peliculas': peliculas,
            'generos': Genero.objects.all(),
            'busqueda': busqueda,
            'genero_id': genero_id,
        },
    )


def detalle(request, pk):
    pelicula = get_object_or_404(
        Pelicula.objects.select_related('genero'),
        pk=pk,
        en_cartelera=True,
    )

    return render(
        request,
        'cartelera/detalle.html',
        {'pelicula': pelicula},
    )