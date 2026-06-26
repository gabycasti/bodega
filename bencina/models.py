from django.db import models
from empleado.models import Empleado


class Bencina(models.Model):
    rut = models.CharField(max_length=15)
    vehiculo = models.CharField(max_length=100)
    monto = models.PositiveIntegerField()
    kilometraje = models.PositiveIntegerField()
    recibo = models.ImageField(upload_to='recibos/')
    fecha_creacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bencina'
        managed = False   
        



class ControlTarjeta(models.Model):
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name="controles_tarjeta"
    )

    fecha = models.DateTimeField(auto_now_add=True)

    hora_checkin = models.TimeField()
    hora_checkout = models.TimeField(null=True, blank=True)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.empleado.nombre} - {self.fecha.date()}"

    class Meta:
        db_table = "control_tarjeta"