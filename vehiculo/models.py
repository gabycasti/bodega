from django.db import models

class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('CAMIONETA', 'CAMIONETA'),
        ('CAMION_LIVIANO', 'CAMIÓN LIVIANO'),
        ('CAMION', 'CAMION'),
        ('TODO_TERRENO', 'TODO TERRENO'),
        ('FURGON', 'FURGON'),
    ]

    tipo_vehiculo = models.CharField(
        max_length=30,
        choices=TIPO_VEHICULO_CHOICES,
        blank=True,
        null=True
    )



    patente = models.CharField(
        max_length=10,
        unique=True
    )

    marca = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    modelo = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    anio = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    n_motor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    carga = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    propietario = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    lugar_mantencion = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patente} - {self.marca or ''} {self.modelo or ''}"

    class Meta:
        db_table = "vehiculos"
        ordering = ["patente"]