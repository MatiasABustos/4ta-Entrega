from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Curso(models.Model):

    nombre = models.CharField(max_length=48)
    camada = models.IntegerField()
    nivel = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"Nombre: {self.nombre}  Camada: {self.camada}  nivel: {self.nivel}"
    
class Avatar(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares" , null=True , blank=True)