from .models import Bencina
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db import connection
from .models import Empleado,ControlTarjeta
from vehiculo.models import Vehiculo
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.db.models.functions import Coalesce
from django.db.models import Q




# LISTADO BENCINA
def listado(request):
    buscar = request.GET.get("buscar", "")

    sql = """
        SELECT 
            b.id,
            b.rut,
            b.vehiculo,
            b.monto,
            b.kilometraje,
            b.recibo,
            b.fecha_creacion,
            e.nombre
        FROM bencina b
        LEFT JOIN empleados e ON e.rut = b.rut
    """

    parametros = []

    if buscar:
        sql += """
            WHERE
                e.nombre ILIKE %s
                OR b.rut ILIKE %s
                OR b.vehiculo ILIKE %s
        """

        parametros.extend([
            f"%{buscar}%",
            f"%{buscar}%",
            f"%{buscar}%"
        ])

    sql += " ORDER BY b.fecha_creacion DESC"

    with connection.cursor() as cursor:
        cursor.execute(sql, parametros)

        columnas = [col[0] for col in cursor.description]
        bencinas = [
            dict(zip(columnas, row))
            for row in cursor.fetchall()
        ]

    return render(request, "bencina_listado.html", {
        "bencinas": bencinas,
        "buscar": buscar,
    })







#ELIMINAR BENCINA
def eliminar_bencina(request, id):
    registro = get_object_or_404(Bencina, id=id)
    registro.delete()
    return redirect('bencina_listado')  # ajusta al nombre de tu vista listado






# ENTREGAR TARJETA BENCINA
def entrega_tarjeta(request):
    empleados = Empleado.objects.filter(activo=True, cargo__iexact="chofer")
    vehiculos = Vehiculo.objects.all()

    if request.method == "POST":
        empleado_id = request.POST.get("empleado_id")
        vehiculo_id = request.POST.get("vehiculo_id")

        if not empleado_id or not vehiculo_id:
            return redirect("entrega_tarjeta")

        empleado = get_object_or_404(Empleado, id=empleado_id)
        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        fecha = request.POST.get("fecha_editable")

        if fecha:
            fecha_guardar = datetime.combine(
                parse_date(fecha),
                time.min
            )
        else:
            fecha_guardar = timezone.now()

        fecha_hasta = request.POST.get("fecha_hasta")

        ControlTarjeta.objects.create(
            empleado=empleado,
            vehiculo=vehiculo,
            fecha_editable=fecha_guardar,
            fecha_hasta=parse_date(fecha_hasta) if fecha_hasta else None,
            hora_checkin=request.POST.get("hora_entrega") or None,
            hora_checkout=request.POST.get("hora_recepcion") or None,
            activo=True
        )

        return redirect("tarjeta_listado")

    return render(request, "entrega_tarjeta.html", {
        "empleados": empleados,
        "vehiculos": vehiculos,
        "fecha_actual": timezone.now(),
    })





# EDITAR TARJETA
def editar_tarjeta(request, id):
    registro = get_object_or_404(ControlTarjeta, id=id)
    empleados = Empleado.objects.filter(activo=True, cargo__iexact="chofer")
    vehiculos = Vehiculo.objects.all()

    if request.method == "POST":
        empleado_id = request.POST.get("empleado_id")
        vehiculo_id = request.POST.get("vehiculo_id")

        registro.empleado = get_object_or_404(Empleado, id=empleado_id)
        registro.vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
        registro.hora_checkin = request.POST.get("hora_entrega") or None
        registro.hora_checkout = request.POST.get("hora_recepcion") or None

        fecha = request.POST.get("fecha_editable")
        if fecha:
            registro.fecha_editable = datetime.combine(parse_date(fecha), time.min)

        fecha_hasta = request.POST.get("fecha_hasta")
        if fecha_hasta:
            registro.fecha_hasta = parse_date(fecha_hasta)

        # Si el checkbox está marcado significa que NO utilizó la tarjeta
        registro.uso_tarjeta = not bool(request.POST.get("no_uso_tarjeta"))

        registro.save()
        return redirect("tarjeta_listado")

    return render(request, "editar_tarjeta.html", {
        "registro": registro,
        "empleados": empleados,
        "vehiculos": vehiculos,
    })







# LISTADO TARJETA
def tarjeta_listado(request):
    buscar = request.GET.get("buscar", "")

    tarjetas = (
        ControlTarjeta.objects
        .annotate(
            fecha_orden=Coalesce("fecha_editable", "fecha")
        )
    )

    if buscar:
        tarjetas = tarjetas.filter(
            Q(empleado__nombre__icontains=buscar) |
            Q(empleado__rut__icontains=buscar) |
            Q(vehiculo__patente__icontains=buscar)
        )

    tarjetas = tarjetas.order_by("-fecha_orden")

   

    return render(request, "tarjeta_listado.html", {
        "tarjetas": tarjetas,
        "buscar": buscar,
    })




def eliminar_tarjeta(request, id):
    registro = get_object_or_404(ControlTarjeta, id=id)
    registro.delete()
    return redirect('tarjeta_listado')