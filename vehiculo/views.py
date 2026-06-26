from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Vehiculo



def vehiculo_listado(request):
    vehiculos = Vehiculo.objects.all().order_by('patente')

    return render(request, 'vehiculo_listado.html', {
        'vehiculos': vehiculos
    })


def registro_vehiculo(request):
    if request.method == 'POST':
        patente = request.POST.get('patente')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        carga = request.POST.get('carga')

        activo = request.POST.get('activo') == 'on'

        Vehiculo.objects.create(
            patente=patente,
            marca=marca,
            carga=carga,
            modelo=modelo,
            activo=activo
        )

        return redirect('vehiculo_listado')

    return render(request, 'registro_vehiculo.html')
