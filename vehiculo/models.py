from django.db import models

class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    carga = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patente} - {self.marca or ''} {self.modelo or ''}"

    class Meta:
        db_table = "vehiculos"
        ordering = ["patente"]