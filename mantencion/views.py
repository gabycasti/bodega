from django.shortcuts import render
from .models import Mantencion
from vehiculo.models import Vehiculo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse



# LISTADO MANTENCIÓN

def listado_mantencion(request):

    mantenciones = Mantencion.objects.select_related(
        "vehiculo"
    ).prefetch_related(
        "vehiculo__permisos_circulacion",
        "vehiculo__seguros"
    ).all()

    hoy = date.today()
    limite = hoy + timedelta(days=30)

    for p in mantenciones:

        # REVISIÓN TÉCNICA
        p.rt_proxima = False
        p.rt_vencida = False

        if p.fecha_revision_tecnica:

            if p.fecha_revision_tecnica < hoy:
                p.rt_vencida = True

            elif p.fecha_revision_tecnica <= limite:
                p.rt_proxima = True


        # GASES
        p.gases_proxima = False
        p.gases_vencida = False

        if p.fecha_gases:

            if p.fecha_gases < hoy:
                p.gases_vencida = True

            elif p.fecha_gases <= limite:
                p.gases_proxima = True


        # SEGURO
        p.seguro_proxima = False
        p.seguro_vencido = False

        seguro = p.vehiculo.seguros.first()

        if seguro and seguro.fecha_vencimiento:

            if seguro.fecha_vencimiento < hoy:
                p.seguro_vencido = True

            elif seguro.fecha_vencimiento <= limite:
                p.seguro_proxima = True


        # PERMISO DE CIRCULACIÓN
        for permiso in p.vehiculo.permisos_circulacion.all():

            permiso.pc_proximo = False
            permiso.pc_vencido = False

            if permiso.fecha_vencimiento:

                if permiso.fecha_vencimiento < hoy:
                    permiso.pc_vencido = True

                elif permiso.fecha_vencimiento <= limite:
                    permiso.pc_proximo = True


        # CAMBIO DE ACEITE
        p.aceite_1000 = False
        p.aceite_500 = False
        p.aceite_300 = False
        p.aceite_vencido = False

        if (
            p.kilometraje is not None
            and p.kilometraje_cambio_aceite is not None
        ):

            faltan = p.kilometraje_cambio_aceite - p.kilometraje

            if faltan <= 0:
                p.aceite_vencido = True

            elif faltan <= 300:
                p.aceite_300 = True

            elif faltan <= 500:
                p.aceite_500 = True

            elif faltan <= 1000:
                p.aceite_1000 = True


    return render(
        request,
        "listado_mantencion.html",
        {"mantenciones": mantenciones}
    )






# EXPORTAR MANTENCIONES A EXCEL

def exportar_mantenciones_excel(request):

    mantenciones = Mantencion.objects.select_related(
        "vehiculo"
    ).prefetch_related(
        "vehiculo__permisos_circulacion"
    ).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Mantenciones"

    # ==========================================================
    # CONFIGURACIÓN GENERAL
    # ==========================================================

    ws.sheet_view.showGridLines = False

    # ==========================================================
    # ENCABEZADOS
    # ==========================================================

    encabezados = [
        "PATENTE",
        "MARCA",
        "MODELO",
        "PROPIETARIO",
        "FECHA RT",
        "GASES",
        "CARGA",
        "PERMISO CIRCULACIÓN",
        "KM",
        "CAMBIO ACEITE",
        "MUNI",
        "LUGAR MANTENCIÓN",

      
    ]

    # Los encabezados comienzan ahora en la fila 2
    for columna, encabezado in enumerate(encabezados, start=1):
        celda = ws.cell(
            row=2,
            column=columna,
            value=encabezado
        )

        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="D9D9D9"
        )

        celda.font = Font(
            color="FFFFFF",
            bold=True,
            size=10
        )

        celda.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

        celda.border = Border(
            left=Side(style="thin", color="FFFFFF"),
            right=Side(style="thin", color="FFFFFF"),
            top=Side(style="thin", color="FFFFFF"),
            bottom=Side(style="thin", color="FFFFFF")
        )

    ws.row_dimensions[2].height = 35

    # ==========================================================
    # DATOS
    # ==========================================================

    for numero, p in enumerate(mantenciones, start=1):

        
        print(
            "PATENTE:", p.vehiculo.patente,
            "| MARCA:", p.vehiculo.marca,
            "| PROPIETARIO:", p.vehiculo.propietario,
            "| LUGAR:", p.vehiculo.lugar_mantencion
        )


        permiso = p.vehiculo.permisos_circulacion.first()

        fecha_permiso = ""
        municipalidad = ""

        if permiso:

            if permiso.fecha_vencimiento:
                fecha_permiso = permiso.fecha_vencimiento

            if permiso.municipalidad:
                municipalidad = permiso.municipalidad

        fila = [
            p.vehiculo.patente or "",
            p.vehiculo.marca or "",
            p.vehiculo.modelo or "",
            p.vehiculo.propietario or "",
            p.fecha_revision_tecnica or "",
            p.fecha_gases or "",
            p.vehiculo.carga or "",
            fecha_permiso,
            p.kilometraje if p.kilometraje is not None else "",
            p.kilometraje_cambio_aceite
            if p.kilometraje_cambio_aceite is not None else "",
            municipalidad,
            p.vehiculo.lugar_mantencion or "",
        ]

        ws.append(fila)

    # ==========================================================
    # BORDES Y FORMATO DE DATOS
    # ==========================================================

    borde = Border(
        left=Side(style="thin", color="B7B7B7"),
        right=Side(style="thin", color="B7B7B7"),
        top=Side(style="thin", color="B7B7B7"),
        bottom=Side(style="thin", color="B7B7B7")
    )

    for fila in ws.iter_rows(
        min_row=3,
        max_row=ws.max_row,
        min_col=1,
        max_col=12
    ):

        for celda in fila:

            celda.border = borde

            celda.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )

            celda.font = Font(
                size=10
            )

    # ==========================================================
    # FILAS ALTERNADAS
    # ==========================================================

    for numero_fila in range(3, ws.max_row + 1):

        if numero_fila % 2 == 0:

            for columna in range(1, 13):

                ws.cell(
                    row=numero_fila,
                    column=columna
                ).fill = PatternFill(
                    fill_type="solid",
                    fgColor="EAF2F8"
                )

    # ==========================================================
    # FORMATO DE FECHAS
    # ==========================================================

    columnas_fecha = [5, 6, 8]

    for fila in range(3, ws.max_row + 1):

        for columna in columnas_fecha:

            celda = ws.cell(
                row=fila,
                column=columna
            )

            if celda.value:

                celda.number_format = "DD/MM/YYYY"

    # ==========================================================
    # FORMATO DE NÚMEROS
    # ==========================================================

    for fila in range(3, ws.max_row + 1):

        # KM
        ws.cell(
            row=fila,
            column=9
        ).number_format = '#,##0'

        # ACEITE
        ws.cell(
            row=fila,
            column=10
        ).number_format = '#,##0'

    # ==========================================================
    # ANCHO DE COLUMNAS
    # ==========================================================

    anchos = {
        "A": 12,
        "B": 15,
        "C": 18,
        "D": 25,
        "E": 15,
        "F": 15,
        "G": 12,
        "H": 20,
        "I": 15,
        "J": 20,
        "K": 22,
        "L": 25,
    }

    for columna, ancho in anchos.items():

        ws.column_dimensions[columna].width = ancho

    # ==========================================================
    # ALTURA DE LAS FILAS
    # ==========================================================

    for fila in range(3, ws.max_row + 1):

        ws.row_dimensions[fila].height = 28

    # ==========================================================
    # CONGELAR ENCABEZADOS
    # ==========================================================

    ws.freeze_panes = "A3"

    # ==========================================================
    # FILTROS
    # ==========================================================

    if ws.max_row >= 2:

        ws.auto_filter.ref = (
           f"A2:L{ws.max_row}"
        )

    # ==========================================================
    # CONFIGURACIÓN DE IMPRESIÓN
    # ==========================================================

    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ws.page_margins.left = 0.25
    ws.page_margins.right = 0.25
    ws.page_margins.top = 0.50
    ws.page_margins.bottom = 0.50

    # ==========================================================
    # REPETIR ENCABEZADOS AL IMPRIMIR
    # ==========================================================

    ws.print_title_rows = "1:2"

    # ==========================================================
    # ÁREA DE IMPRESIÓN
    # ==========================================================

    if ws.max_row >= 2:

       ws.print_area = f"A1:L{ws.max_row}"

    # ==========================================================
    # RESPUESTA
    # ==========================================================

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="reporte_mantenciones.xlsx"'
    )

    wb.save(response)

    return response









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