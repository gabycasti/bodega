from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Vehiculo
from django.core.paginator import Paginator



#LISTADO VEHICULO
def vehiculo_listado(request):
    vehiculos = Vehiculo.objects.all().order_by('-carga')


    paginator = Paginator(vehiculos, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    vehiculos = paginator.get_page(page_number)

    return render(request, 'vehiculo_listado.html', {
        'vehiculos': vehiculos
    })


#REGISTRO VEHICULO
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





#EDITAR VEHICULO
def editar_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)

    if request.method == 'POST':
        vehiculo.patente = request.POST.get('patente')
        vehiculo.marca = request.POST.get('marca')
        vehiculo.modelo = request.POST.get('modelo')
        vehiculo.carga = request.POST.get('carga')
        vehiculo.activo = request.POST.get('activo') == 'on'

        vehiculo.save()

        return redirect('vehiculo_listado')

    return render(request, 'editar_vehiculo.html', {
        'vehiculo': vehiculo
    })


#CAMBIAR EL ESTADO DEL VEHICULO
def cambiar_estado_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)

    vehiculo.activo = not vehiculo.activo
    vehiculo.save()

    return redirect('vehiculo_listado')  # Cambia por el nombre de tu vista de listado
