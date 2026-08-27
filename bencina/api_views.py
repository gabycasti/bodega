from django.http import JsonResponse
from django.db import connection


def api_bencina(request):
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

    for b in bencinas:

        if b["fecha_creacion"]:
            b["fecha_creacion"] = b["fecha_creacion"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        if b["recibo"]:
            b["recibo"] = str(b["recibo"])

    return JsonResponse({
        "success": True,
        "bencinas": bencinas
    })