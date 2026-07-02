from django.db import models
from empleado.models import Empleado


class Documento(models.Model):

    TIPOS_DOCUMENTO = [
        ('CI', 'Carnet de Identidad'),
        ('LIC', 'Licencia de Conducir'),
        ('HIST', 'Hoja del Conductor'),
    ]

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPOS_DOCUMENTO
    )

    archivo = models.FileField(upload_to='documentos/')

    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    observacion = models.TextField(blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.nombre} - {self.get_tipo_documento_display()}"

    class Meta:
        db_table = 'documentos'