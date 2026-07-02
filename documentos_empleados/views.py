from django.shortcuts import render, redirect
from empleado.models import Empleado
from .models import Documento



#LISTADO DOCUMENTOS
def listado_documento(request):
    documentos = Documento.objects.select_related('empleado').all().order_by('-id')

    return render(request, "listado_documentos.html", {
        "documentos": documentos
    })




#CREAR DOCUMENTOS
def crear_documento(request):
    empleados = Empleado.objects.all()

    if request.method == "POST":
        empleado_id = request.POST.get("empleado")
        tipo_documento = request.POST.get("tipo_documento")
        archivo = request.FILES.get("archivo")
        fecha_emision = request.POST.get("fecha_emision")
        fecha_vencimiento = request.POST.get("fecha_vencimiento")
        observacion = request.POST.get("observacion")

        empleado = Empleado.objects.get(id=empleado_id)

        Documento.objects.create(
            empleado=empleado,
            tipo_documento=tipo_documento,
            archivo=archivo,
            fecha_emision=fecha_emision if fecha_emision else None,
            fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
            observacion=observacion
        )

        return redirect("listado_documento")

    return render(request, "crear_documento.html", {
        "empleados": empleados
    })