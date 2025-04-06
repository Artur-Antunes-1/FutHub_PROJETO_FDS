from django.db import models

# Create your models here.
class Pelada(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    local = models.CharField(max_length=100)
