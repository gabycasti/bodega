from django.db import models

class Bencina(models.Model):
    rut = models.CharField(max_length=15)
    vehiculo = models.CharField(max_length=100)

    monto = models.PositiveIntegerField()
    kilometraje = models.PositiveIntegerField()

    recibo = models.ImageField(upload_to='recibos/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'bencina'

    def __str__(self):
        return f"{self.rut} - {self.vehiculo}"