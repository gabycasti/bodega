from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Seguro
from vehiculo.models import Vehiculo
from django.shortcuts import get_object_or_404





#LISTADO PERMISO DE CIRCULACIÓN
def seguro_listado(request):

    seguros = Seguro.objects.select_related("vehiculo")

    return render(
        request,"seguro_listado.html",{"seguros": seguros,},
    )





#CREAR SEGURO

def seguro(request):

    if request.method == 'POST':

        vehiculo_id = request.POST.get('vehiculo')
        banco = request.POST.get('banco')
        numero_poliza = request.POST.get('numero_poliza')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        archivo = request.FILES.get('archivo')

        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        seguro = Seguro(
            vehiculo=vehiculo,
            banco=banco,
            numero_poliza=numero_poliza,
            fecha_vencimiento=fecha_vencimiento,
            archivo=archivo
        )

        seguro.save()

        messages.success(request, 'Seguro creado correctamente.')

        return redirect('seguro_listado')

    vehiculos = Vehiculo.objects.filter(activo=True).order_by('patente')

    return render(
        request,
        'seguro.html',
        {
            'vehiculos': vehiculos
        }
    )

