from django.db import models

class Empleado(models.Model):

    CARGOS = [
        ("JEFE BODEGA", "JEFE BODEGA"),
        ("SUB ENCARGADO BODEGA", "SUB ENCARGADO BODEGA"),
        ("GESTOR DE FLOTA", "GESTOR DE FLOTA"),
        ("OPERADOR GRUA HORQUILLA", "OPERADOR GRUA HORQUILLA"),
        ("OPERADOR CORTE", "OPERADOR CORTE"),
        ("EMPAQUE", "EMPAQUE"),
        ("CHOFER", "CHOFER"),
        ("PEONETA", "PEONETA"),
    ]

    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    cargo = models.CharField(max_length=50, choices=CARGOS)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

    class Meta:
        db_table = "empleados"