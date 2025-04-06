from django.db import models

# Create your models here.
class Pelada(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    local = models.CharField(max_length=100)

class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    posicao = models.CharField(max_length=50)

class Presenca(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)