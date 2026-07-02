from .models import Empleado
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect




#LISTADO EMPLEADO
def empleado_listado(request):
    empleados = Empleado.objects.all().order_by('-fecha_creacion')

    return render(request, 'empleado_listado.html', {
        'empleados': empleados
    })


#REGISTRO EMPLEADO
def registro_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        cargo = request.POST.get('cargo')

        activo = request.POST.get('activo') == 'on'

        Empleado.objects.create(
            nombre=nombre,
            rut=rut,
            cargo=cargo,
            activo=activo
        )

        return redirect('empleado_listado')

    return render(request, 'registro_empleado.html')



#EDITAR EMPLEADO
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.rut = request.POST.get('rut')
        empleado.cargo = request.POST.get('cargo')
        empleado.activo = request.POST.get('activo') == 'on'

        empleado.save()

        return redirect('empleado_listado')

    return render(request, 'editar_empleado.html', {
        'empleado': empleado
    })


# CAMBIAR ESTADO EMPLEADO
def cambiar_estado_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if empleado.activo:
        empleado.activo = False
    else:
        empleado.activo = True

    empleado.save()

    return redirect('empleado_listado')

