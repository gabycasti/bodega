from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PermisoCirculacion
from vehiculo.models import Vehiculo



def gestion_listado(request):

    permisos = PermisoCirculacion.objects.select_related("vehiculo")

    return render(
        request,"gestion_listado.html",{"permisos": permisos,},
    )





def permiso_circulacion(request):
    vehiculos = Vehiculo.objects.filter(activo=True).order_by("patente")

    if request.method == "POST":
        vehiculo_id = request.POST.get("vehiculo")
        municipalidad = request.POST.get("municipalidad")
        fecha_emision = request.POST.get("fecha_emision")
        fecha_vencimiento = request.POST.get("fecha_vencimiento")
        observacion = request.POST.get("observacion")
        archivo = request.FILES.get("archivo")

        try:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)

            PermisoCirculacion.objects.create(
                vehiculo=vehiculo,
                municipalidad=municipalidad,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento,
                archivo=archivo,
                observacion=observacion
            )

            messages.success(request, "Permiso de circulación registrado correctamente.")
            return redirect("gestion_listado")

        except Vehiculo.DoesNotExist:
            messages.error(request, "Debe seleccionar un vehículo válido.")

    return render(
        request,
        "permiso_circulacion.html",
        {
            "vehiculos": vehiculos
        }
    )