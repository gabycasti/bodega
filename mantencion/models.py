from django.db import models
from vehiculo.models import Vehiculo




class Mantencion(models.Model):

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="mantenciones"
    )

    fecha_revision_tecnica = models.DateField(
        null=True,
        blank=True
    )


    archivo_revision_tecnica = models.FileField(
        upload_to="mantenciones/revision_tecnica/",
        null=True,
        blank=True
    )


    fecha_gases = models.DateField(
        null=True,
        blank=True
    )



    archivo_gases = models.FileField(
        upload_to="mantenciones/gases/",
        null=True,
        blank=True
    )


    kilometraje = models.IntegerField(
        null=True,
        blank=True
    )

   
    kilometraje_cambio_aceite = models.IntegerField(
        null=True,
        blank=True
    )


    observacion = models.TextField(
        blank=True
    )


    class Meta:
        db_table = "mantenciones"
        
