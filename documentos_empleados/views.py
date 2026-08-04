from django.shortcuts import render, redirect
from empleado.models import Empleado
from .models import Documento
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta




# LISTADO DOCUMENTOS
def listado_documentos(request):
    empleados = (
        Empleado.objects
        .filter(bodega="ALDUNATE")
        .prefetch_related('documentos')
        .order_by('-id')
    )

    hoy = date.today()
    un_mes = hoy + timedelta(days=30)

    for emp in empleados:
        emp.licencia = emp.documentos.filter(tipo_documento='LIC').first()
        emp.hoja = emp.documentos.filter(tipo_documento='HIST').first()

        # Licencia
        emp.alerta_licencia = False
        if (
            emp.licencia
            and emp.licencia.fecha_vencimiento
            and emp.licencia.fecha_vencimiento <= un_mes
        ):
            emp.alerta_licencia = True

        # Hoja del conductor (opcional)
        emp.alerta_hoja = False
        if (
            emp.hoja
            and emp.hoja.fecha_vencimiento
            and emp.hoja.fecha_vencimiento <= un_mes
        ):
            emp.alerta_hoja = True

    return render(request, "listado_documentos.html", {
        "empleados": empleados
    })



# LISTADO SAN FRANCISCO
def listado_francisco(request):
    empleados = (
        Empleado.objects
        .filter(bodega="SAN FRANCISCO")
        .prefetch_related('documentos')
        .order_by('-id')
    )

    hoy = date.today()
    un_mes = hoy + timedelta(days=30)

    for emp in empleados:
        emp.licencia = emp.documentos.filter(tipo_documento='LIC').first()
        emp.hoja = emp.documentos.filter(tipo_documento='HIST').first()

        # Alerta licencia
        emp.alerta_licencia = False
        if (
            emp.licencia
            and emp.licencia.fecha_vencimiento
            and emp.licencia.fecha_vencimiento <= un_mes
        ):
            emp.alerta_licencia = True

        # Alerta hoja conductor
        emp.alerta_hoja = False
        if (
            emp.hoja
            and emp.hoja.fecha_vencimiento
            and emp.hoja.fecha_vencimiento <= un_mes
        ):
            emp.alerta_hoja = True

    return render(request, "listado_francisco.html", {
        "empleados": empleados
    })






# LISTADO VIEL
def listado_viel(request):
    empleados = (
        Empleado.objects
        .filter(bodega="VIEL")
        .prefetch_related('documentos')
        .order_by('-id')
    )

    hoy = date.today()
    un_mes = hoy + timedelta(days=30)

    for emp in empleados:
        emp.licencia = emp.documentos.filter(tipo_documento='LIC').first()
        emp.hoja = emp.documentos.filter(tipo_documento='HIST').first()

        # Alerta licencia
        emp.alerta_licencia = False
        if (
            emp.licencia
            and emp.licencia.fecha_vencimiento
            and emp.licencia.fecha_vencimiento <= un_mes
        ):
            emp.alerta_licencia = True

        # Alerta hoja conductor
        emp.alerta_hoja = False
        if (
            emp.hoja
            and emp.hoja.fecha_vencimiento
            and emp.hoja.fecha_vencimiento <= un_mes
        ):
            emp.alerta_hoja = True

    return render(request, "listado_viel.html", {
        "empleados": empleados
    })












# CREAR DOCUMENTOS
def crear_documento(request):
    empleados = Empleado.objects.all()

    if request.method == "POST":

        empleado_id = request.POST.get("empleado_id")
        observacion = request.POST.get("observacion")

        empleado = Empleado.objects.get(id=empleado_id)


        # LICENCIA
        Documento.objects.create(
            empleado=empleado,
            tipo_documento="LIC",
            archivo=request.FILES.get("archivo_lic_frente"),
            archivo_reverso=request.FILES.get("archivo_lic_reverso"),
            fecha_vencimiento=request.POST.get("fecha_vencimiento_lic") or None,
            observacion=observacion
        )


        # HOJA CONDUCTOR
        Documento.objects.create(
            empleado=empleado,
            tipo_documento="HIST",
            archivo=request.FILES.get("archivo_hist_frente"),
            archivo_reverso=request.FILES.get("archivo_hist_reverso"),
            fecha_vencimiento=request.POST.get("fecha_vencimiento_hist") or None,
            observacion=observacion
        )


        
       # CI
        if request.FILES.get("archivo_ci_frente"):
            Documento.objects.create(
                empleado=empleado,
                tipo_documento="CI",
                archivo=request.FILES.get("archivo_ci_frente"),
                archivo_reverso=request.FILES.get("archivo_ci_reverso"),
                fecha_vencimiento=request.POST.get("fecha_vencimiento_ci") or None,
                observacion=observacion
            )


        return redirect("listado_documentos")


    return render(request, "crear_documento.html", {
        "empleados": empleados
    })








# EDITAR DOCUMENTOS
def editar_documento(request, id):

    empleado = get_object_or_404(
        Empleado,
        id=id
    )

    documentos = {
        "CI": empleado.documentos.filter(tipo_documento="CI").first(),
        "LIC": empleado.documentos.filter(tipo_documento="LIC").first(),
        "HIST": empleado.documentos.filter(tipo_documento="HIST").first(),
    }


    if request.method == "POST":

        observacion = request.POST.get("observacion")

        


        archivos = [
            ("CI", "archivo_ci", "fecha_vencimiento_ci"),
            ("LIC", "archivo_lic", "fecha_vencimiento_lic"),
            ("HIST", "archivo_hist_frente", "fecha_vencimiento_hist"),
        ]


        for tipo, campo_archivo, campo_fecha in archivos:

            archivo = request.FILES.get(campo_archivo)
            fecha_vencimiento = request.POST.get(campo_fecha)

            documento = documentos[tipo]


            # Define reverso según documento
            archivo_reverso = None

            if tipo == "CI":
                archivo_reverso = request.FILES.get("archivo_ci_reverso")

            elif tipo == "LIC":
                archivo_reverso = request.FILES.get("archivo_lic_reverso")

            elif tipo == "HIST":
                archivo_reverso = request.FILES.get("archivo_hist_reverso")


            if documento:

                # Actualiza frente
                if archivo:
                    documento.archivo = archivo


                # Actualiza reverso
                if archivo_reverso:
                    documento.archivo_reverso = archivo_reverso


                # Actualiza fecha
                documento.fecha_vencimiento = (
                    fecha_vencimiento
                    if fecha_vencimiento else None
                )


                documento.observacion = observacion
                documento.save()


            else:

                # Crear documento si no existe
                if archivo:

                    Documento.objects.create(
                        empleado=empleado,
                        tipo_documento=tipo,
                        archivo=archivo,
                        archivo_reverso=archivo_reverso,
                        fecha_vencimiento=(
                            fecha_vencimiento
                            if fecha_vencimiento else None
                        ),
                        observacion=observacion
                    )


        return redirect("listado_documentos")


    return render(request, "editar_documento.html", {
        "empleado": empleado,
        "documentos": documentos
    })