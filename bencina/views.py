from .models import Bencina
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db import connection
from .models import Empleado,ControlTarjeta


#LISTADO BENCINA
def listado(request):
    with connection.cursor() as cursor:
        cursor.execute("""
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
            ORDER BY b.fecha_creacion DESC
        """)

        columnas = [col[0] for col in cursor.description]
        bencinas = [
            dict(zip(columnas, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'bencina_listado.html', {
        'bencinas': bencinas
    })




#ELIMINAR BENCINA
def eliminar_bencina(request, id):
    registro = get_object_or_404(Bencina, id=id)
    registro.delete()
    return redirect('bencina_listado')  # ajusta al nombre de tu vista listado




#ENTREGAR TARJETA BENCINA
def entrega_tarjeta(request):
    empleados = Empleado.objects.filter(activo=True, cargo__iexact="chofer")
    
    if request.method == "POST":
        empleado_id = request.POST.get("empleado_id")

        if not empleado_id:
            return redirect("entrega_tarjeta")

        empleado = get_object_or_404(Empleado, id=empleado_id)

        ControlTarjeta.objects.create(
            empleado=empleado,
            hora_checkin=request.POST.get("hora_entrega") or None,
            hora_checkout=request.POST.get("hora_recepcion") or None
        )

        return redirect("entrega_tarjeta")

    return render(request, "entrega_tarjeta.html", {
        "empleados": empleados
    })



#LISTADO TATJETA
def tarjeta_listado(request):
    tarjetas = ControlTarjeta.objects.all().order_by('-fecha')

    return render(request, 'tarjeta_listado.html', {
        'tarjetas': tarjetas
    })
