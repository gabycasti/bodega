from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Seguro
from vehiculo.models import Vehiculo
from django.shortcuts import get_object_or_404
from datetime import date, timedelta




# LISTADO SEGURO
def seguro_listado(request):

    seguros = Seguro.objects.select_related("vehiculo")

    hoy = date.today()
    limite = hoy + timedelta(days=30)

    for seguro in seguros:
        seguro.alerta_vencimiento = (
            seguro.fecha_vencimiento <= limite
        )

    return render(
        request,
        "seguro_listado.html",
        {
            "seguros": seguros,
        },
    )









#CREAR SEGURO

def seguro(request):

    if request.method == 'POST':

        vehiculo_id = request.POST.get('vehiculo')
        banco = request.POST.get('banco')
        numero_poliza = request.POST.get('numero_poliza')
        item = request.POST.get('item')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        archivo = request.FILES.get('archivo')

        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        seguro = Seguro(
            vehiculo=vehiculo,
            banco=banco,
            numero_poliza=numero_poliza,
            item=item,
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





# EDITAR SEGURO
def editar_seguro(request, id):

    seguro = get_object_or_404(Seguro, id=id)

    if request.method == 'POST':

        vehiculo_id = request.POST.get('vehiculo')
        banco = request.POST.get('banco')
        numero_poliza = request.POST.get('numero_poliza')
        item = request.POST.get('item')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        archivo = request.FILES.get('archivo')

        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        seguro.vehiculo = vehiculo
        seguro.banco = banco
        seguro.numero_poliza = numero_poliza
        seguro.item = item
        seguro.fecha_vencimiento = fecha_vencimiento

        # Solo cambia el archivo si se seleccionó uno nuevo
        if archivo:
            seguro.archivo = archivo

        seguro.save()

        messages.success(request, 'Seguro actualizado correctamente.')

        return redirect('seguro_listado')

    vehiculos = Vehiculo.objects.filter(
        activo=True
    ).order_by('patente')

    return render(
        request,
        'editar_seguro.html',
        {
            'seguro': seguro,
            'vehiculos': vehiculos
        }
    )




# ELIMINAR SEGURO

def eliminar_seguro(request, id):

    seguro = get_object_or_404(Seguro, id=id)

    seguro.delete()

    messages.success(request, 'Seguro eliminado correctamente.')

    return redirect('seguro_listado')
