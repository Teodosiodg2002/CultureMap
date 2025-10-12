from django.shortcuts import render
from .models import Lugar

def index(request):
    lugares = Lugar.objects.all()  # Trae todos los lugares de la base de datos
    return render(request, 'lugares/index.html', {'lugares': lugares})
