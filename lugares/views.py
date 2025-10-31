from django.shortcuts import redirect, render, get_object_or_404
from .models import Lugar, EstadoAprobacion
from .forms import LugarForm
from django.contrib.auth.decorators import login_required


def listar_lugares_todos(request):
    lugares = Lugar.objects.all()  # Trae todos los lugares de la base de datos
    return render(request, "lugares/listar_lugares_todos.html", {"lugares": lugares})


# lugares/views.py

def listar_lugares_aprobados(request):
    
    lugares_aprobados = Lugar.objects.filter(estado=EstadoAprobacion.APROBADO, publicado=True)

    lugares_para_mapa = lugares_aprobados.exclude(lat__isnull=True, lng__isnull=True)

    context = {
        'lugares': lugares_aprobados,
        'lugares_para_mapa': lugares_para_mapa  
    }
    return render(request, 'lugares/listar_lugares_aprobados.html', context)


def detalle_lugar(request, pk):
    lugar = get_object_or_404(
        Lugar, pk=pk, estado=EstadoAprobacion.APROBADO, publicado=True
    )
    return render(request, "lugares/detalle_lugar.html", {"lugar": lugar})


@login_required
def crear_lugar(request):
    if request.method == "POST":

        form = LugarForm(request.POST)

        if form.is_valid():

            lugar = form.save(commit=False)

            lugar.creado_por = request.user
            lugar.estado = EstadoAprobacion.PENDIENTE

            lugar.save()

            return redirect("detalle_lugar", pk=lugar.pk)

    else:
        form = LugarForm()

    return render(request, "lugares/crear_lugar.html", {"form": form})
