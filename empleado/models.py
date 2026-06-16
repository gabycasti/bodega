from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    cargo = models.CharField(max_length=50)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

    class Meta:
        db_table = 'empleados'