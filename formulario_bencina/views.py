from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .models import Bencina


def home(request):
    return render(request, 'home.html')


def rut_existe(rut):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM empleados WHERE rut = %s",
            [rut]
        )
        return cursor.fetchone() is not None




def registro_bencina(request):

    if request.method == 'POST':

        rut = request.POST.get('rut', '').strip()
        vehiculo = request.POST.get('vehiculo', '').strip()
        recibo = request.FILES.get('recibo')

        monto = request.POST.get("monto", "").strip()
        kilometraje = request.POST.get("kilometraje", "").strip()

        # Validar RUT existe en Empleados
        if not rut_existe(rut):
            return render(request, 'home.html', {
                'error': 'El RUT no existe en empleados',
                'form_data': request.POST
            })

        # validar números
        if not monto.isdigit() or not kilometraje.isdigit():
            return render(request, 'home.html', {
                'error': 'Datos inválidos.',
                'form_data': request.POST
            })


        Bencina.objects.create(
            rut=rut,
            vehiculo=vehiculo,
            monto=int(monto),
            kilometraje=int(kilometraje),
            recibo=recibo
        )

        messages.success(request, "Registro enviado correctamente 🚗")
        return redirect('registro_bencina')

    return render(request, 'home.html')