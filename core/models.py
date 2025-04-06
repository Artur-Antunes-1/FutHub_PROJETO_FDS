from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pelada(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField(default='18:00:00')  
    local = models.CharField(max_length=100)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.data} {self.hora}"
    def get_data_completa(self):
        return f"{self.data} {self.hora}"

class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    posicao = models.CharField(max_length=50)

class Presenca(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)