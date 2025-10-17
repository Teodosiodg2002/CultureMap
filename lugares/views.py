from django.shortcuts import render, get_object_or_404
from .models import Lugar, EstadoAprobacion

def listar_lugares_todos(request):
    lugares = Lugar.objects.all()  # Trae todos los lugares de la base de datos
    return render(request, 'lugares/listar_lugares_todos.html', {'lugares': lugares})

def listar_lugares_aprobados(request):
    lugares = Lugar.objects.filter(estado=EstadoAprobacion.APROBADO, publicado=True)
    return render(request, 'lugares/listar_lugares_aprobados.html', {'lugares': lugares} )

def detalle_lugar(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk, estado=EstadoAprobacion.APROBADO, publicado=True)
    return render(request, "lugares/detalle_lugar.html", {'lugar': lugar})
    