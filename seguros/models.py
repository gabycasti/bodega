from django.db import models
from vehiculo.models import Vehiculo


class Seguro(models.Model):

    BANCO_CHOICES = [
        ('BCI', 'Banco BCI'),
    ]

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='seguros'
    )

    item = models.CharField(
        max_length=100,
        blank=True
    )

    banco = models.CharField(
        max_length=50,
        choices=BANCO_CHOICES,
        default='BCI'
    )

    numero_poliza = models.CharField(
        max_length=100
    )

    fecha_vencimiento = models.DateField()

    archivo = models.FileField(
        upload_to='seguros/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.vehiculo.patente} - Póliza {self.numero_poliza}"