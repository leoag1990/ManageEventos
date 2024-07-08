from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    describe = models.TextField()
    ubica = models.URLField(unique=False, blank=True)
    fecha = models.DateTimeField()
    usuario_creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evento_creado', null=False,
                                        blank=False)

    def __str__(self):
        return self.nombre


class Inscrito(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_id', null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_id', null=False, blank=False)
    fecha_inscribe = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} inscrito a {self.evento}"
