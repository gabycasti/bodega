from .models import Empleado
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect


def empleado_listado(request):
    empleados = Empleado.objects.all().order_by('-fecha_creacion')

    return render(request, 'empleado_listado.html', {
        'empleados': empleados
    })


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


