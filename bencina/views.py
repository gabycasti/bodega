from .models import Bencina
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db import connection


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






def eliminar_bencina(request, id):
    registro = get_object_or_404(Bencina, id=id)
    registro.delete()
    return redirect('bencina_listado')  # ajusta al nombre de tu vista listado