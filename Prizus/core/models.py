from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Modelo Comentarios de Usuarios

class comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username}"