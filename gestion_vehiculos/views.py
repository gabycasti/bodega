
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PermisoCirculacion
from vehiculo.models import Vehiculo
from django.shortcuts import get_object_or_404





#LISTADO PERMISO DE CIRCULACIÓN
def gestion_listado(request):

    permisos = PermisoCirculacion.objects.select_related("vehiculo")

    return render(
        request,"gestion_listado.html",{"permisos": permisos,},
    )





#CREAR PERMISO DE CIRCULACIÓN
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





# EDITAR PERMISO CIRCULACIÓN
def editar_permiso_circulacion(request, id):

    permiso = get_object_or_404(PermisoCirculacion, id=id)

    vehiculos = Vehiculo.objects.filter(
        activo=True
    ).order_by("patente")

    if request.method == "POST":

        permiso.vehiculo = get_object_or_404(
            Vehiculo,
            id=request.POST.get("vehiculo")
        )

        permiso.municipalidad = request.POST.get("municipalidad")
        permiso.fecha_emision = request.POST.get("fecha_emision")
        permiso.fecha_vencimiento = request.POST.get("fecha_vencimiento")
        permiso.observacion = request.POST.get("observacion")

        archivo = request.FILES.get("archivo")
        if archivo:
            permiso.archivo = archivo

        permiso.save()

        messages.success(
            request,
            "Permiso de circulación actualizado correctamente."
        )

        return redirect("gestion_listado")

    return render(
        request,
        "editar_permiso_circulacion.html",  # o el template que estés usando
        {
            "permiso": permiso,
            "vehiculos": vehiculos,
        },
    )






#ELIMINAR PERMISO
def eliminar_permiso_circulacion(request, id):

    permiso = get_object_or_404(
        PermisoCirculacion,
        id=id
    )

    # Elimina el archivo físico si existe
    if permiso.archivo:
        permiso.archivo.delete(save=False)

    permiso.delete()

    messages.success(
        request,
        "Permiso de circulación eliminado correctamente."
    )

    return redirect("gestion_listado")