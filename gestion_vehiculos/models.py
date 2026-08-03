from django.db import models
from vehiculo.models import Vehiculo


class PermisoCirculacion(models.Model):

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="permisos_circulacion"
    )

    municipalidad = models.CharField(
        max_length=100
    )

    fecha_emision = models.DateField()

    fecha_vencimiento = models.DateField()

    archivo = models.FileField(
        upload_to="permisos_circulacion/"
    )

    observacion = models.TextField(
        blank=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "permisos_circulacion"
        ordering = ["-fecha_vencimiento"]


    def __str__(self):
        return f"{self.vehiculo.patente} - {self.fecha_vencimiento}"