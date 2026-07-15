from django.shortcuts import render, redirect
from empleado.models import Empleado
from .models import Documento
from django.shortcuts import render, redirect, get_object_or_404



# LISTADO DOCUMENTOS
def listado_documentos(request):
    empleados = Empleado.objects.prefetch_related('documentos').all().order_by('-id')

    for emp in empleados:
        emp.licencia = emp.documentos.filter(tipo_documento='LIC').first()
        emp.hoja = emp.documentos.filter(tipo_documento='HIST').first()

    return render(request, "listado_documentos.html", {
        "empleados": empleados
    })





# CREAR DOCUMENTOS
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
        if request.FILES.get("archivo_hist"):
            Documento.objects.create(
                empleado=empleado,
                tipo_documento="HIST",
                archivo=request.FILES.get("archivo_hist"),
                fecha_vencimiento=request.POST.get("fecha_vencimiento_hist") or None,
                observacion=observacion
            )


        # CI (si lo necesitas)
        if request.FILES.get("archivo_ci"):
            Documento.objects.create(
                empleado=empleado,
                tipo_documento="CI",
                archivo=request.FILES.get("archivo_ci"),
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
            ("LIC", "archivo_lic_frente", "fecha_vencimiento_lic"),
            ("HIST", "archivo_hist", "fecha_vencimiento_hist"),
        ]


        for tipo, campo_archivo, campo_fecha in archivos:

            archivo = request.FILES.get(campo_archivo)
            fecha_vencimiento = request.POST.get(campo_fecha)

            documento = documentos[tipo]


            if documento:

                # Actualiza documento existente
                if archivo:
                    documento.archivo = archivo

                # Actualiza reverso de licencia
                if tipo == "LIC":
                    archivo_reverso = request.FILES.get("archivo_lic_reverso")

                    if archivo_reverso:
                        documento.archivo_reverso = archivo_reverso


                documento.fecha_vencimiento = (
                    fecha_vencimiento
                    if fecha_vencimiento else None
                )

                documento.observacion = observacion
                documento.save()


            else:

                # Si no existe lo crea
                if archivo:

                    Documento.objects.create(
                        empleado=empleado,
                        tipo_documento=tipo,
                        archivo=archivo,
                        archivo_reverso=request.FILES.get("archivo_lic_reverso") if tipo == "LIC" else None,
                        fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
                        observacion=observacion
                    )


        return redirect("listado_documentos")


    return render(request, "editar_documento.html", {
        "empleado": empleado,
        "documentos": documentos
    })