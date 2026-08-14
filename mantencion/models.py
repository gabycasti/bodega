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
        





## Telegram
class TelegramDestinatario(models.Model):
    nombre = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre




class TelegramAvisoAceite(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )

    tipo_aviso = models.CharField(
        max_length=20
    )

    fecha_envio = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("vehiculo", "tipo_aviso")

    def __str__(self):
        return f"{self.vehiculo} - {self.tipo_aviso}"