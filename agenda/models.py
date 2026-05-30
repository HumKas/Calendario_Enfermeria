from django.db import models


class Cita(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    nombre = models.CharField(
        max_length=100
    )

    fecha = models.DateField()

    hora = models.TimeField()

    motivo = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente'
    )

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"