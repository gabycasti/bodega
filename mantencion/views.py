from django.shortcuts import render
from .models import Mantencion
from vehiculo.models import Vehiculo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages




#LISTADO MANTENCIÓN

def listado_mantencion(request):

    mantenciones = Mantencion.objects.select_related("vehiculo").all()

    return render( request, "listado_mantencion.html",
        {"mantenciones": mantenciones,} )





# AGREGAR MANTENCIÓN

def agregar_mantencion(request):

    vehiculos = Vehiculo.objects.filter(
        activo=True
    ).order_by("patente")

    if request.method == "POST":

        vehiculo_id = request.POST.get("vehiculo")

        fecha_revision_tecnica = request.POST.get(
            "fecha_revision_tecnica"
        )

        archivo_revision_tecnica = request.FILES.get(
            "archivo_revision_tecnica"
        )

        fecha_gases = request.POST.get(
            "fecha_gases"
        )

        archivo_gases = request.FILES.get(
            "archivo_gases"
        )

        kilometraje = request.POST.get(
            "kilometraje"
        )

        kilometraje_cambio_aceite = request.POST.get(
            "kilometraje_cambio_aceite"
        )

        observacion = request.POST.get(
            "observacion"
        )

        vehiculo = get_object_or_404(
            Vehiculo,
            id=vehiculo_id
        )

        Mantencion.objects.create(
            vehiculo=vehiculo,
            fecha_revision_tecnica=fecha_revision_tecnica or None,
            archivo_revision_tecnica=archivo_revision_tecnica,
            fecha_gases=fecha_gases or None,
            archivo_gases=archivo_gases,
            kilometraje=kilometraje or None,
            kilometraje_cambio_aceite=kilometraje_cambio_aceite or None,
            observacion=observacion
        )

        messages.success(
            request,
            "La mantención fue registrada correctamente."
        )

        return redirect("listado_mantencion")

    return render(
        request,
        "agregar_mantencion.html",
        {
            "vehiculos": vehiculos
        }
    )



# EDITAR MANTENCIÓN
def editar_mantencion(request, id):

    mantencion = get_object_or_404(
        Mantencion,
        id=id
    )

    vehiculos = Vehiculo.objects.filter(
        activo=True
    ).order_by("patente")

    if request.method == "POST":

        vehiculo_id = request.POST.get("vehiculo")

        fecha_revision_tecnica = request.POST.get(
            "fecha_revision_tecnica"
        )

        archivo_revision_tecnica = request.FILES.get(
            "archivo_revision_tecnica"
        )

        fecha_gases = request.POST.get(
            "fecha_gases"
        )

        archivo_gases = request.FILES.get(
            "archivo_gases"
        )

        kilometraje = request.POST.get(
            "kilometraje"
        )

        kilometraje_cambio_aceite = request.POST.get(
            "kilometraje_cambio_aceite"
        )

        observacion = request.POST.get(
            "observacion"
        )

        vehiculo = get_object_or_404(
            Vehiculo,
            id=vehiculo_id
        )

        mantencion.vehiculo = vehiculo
        mantencion.fecha_revision_tecnica = (
            fecha_revision_tecnica or None
        )
        mantencion.fecha_gases = (
            fecha_gases or None
        )
        mantencion.kilometraje = (
            kilometraje or None
        )
        mantencion.kilometraje_cambio_aceite = (
            kilometraje_cambio_aceite or None
        )
        mantencion.observacion = observacion

        # Solo reemplazar archivo si se seleccionó uno nuevo
        if archivo_revision_tecnica:
            mantencion.archivo_revision_tecnica = (
                archivo_revision_tecnica
            )

        if archivo_gases:
            mantencion.archivo_gases = (
                archivo_gases
            )

        mantencion.save()

        messages.success(
            request,
            "La mantención fue actualizada correctamente."
        )

        return redirect("listado_mantencion")

    return render(
        request,
        "editar_mantencion.html",
        {
            "mantencion": mantencion,
            "vehiculos": vehiculos
        }
    )







# ELIMINAR MANTENCIÓN

def eliminar_mantencion(request, id):

    mantencion = get_object_or_404(
        Mantencion,
        id=id
    )

    if request.method == "POST":

        mantencion.delete()

        messages.success(
            request,
            "La mantención fue eliminada correctamente."
        )

        return redirect("listado_mantencion")

    return render(
        request,
        "eliminar_mantencion.html",
        {
            "mantencion": mantencion
        }
    )