from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Pelada(models.Model):
    DIAS_DA_SEMANA = [
        ('0', 'Domingo'),
        ('1', 'Segunda-feira'),
        ('2', 'Terça-feira'),
        ('3', 'Quarta-feira'),
        ('4', 'Quinta-feira'),
        ('5', 'Sexta-feira'),
        ('6', 'Sábado'),
    ]

    nome = models.CharField(max_length=100)
    data_inicial = models.DateField(verbose_name="Data inicial")  # Mudamos de 'data' para 'data_inicial'
    hora = models.TimeField(default='18:00:00')
    local = models.CharField(max_length=100)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Campos novos para recorrência
    recorrente = models.BooleanField(default=False, verbose_name="Pelada semanal?")
    dia_semana = models.CharField(
        max_length=1, 
        choices=DIAS_DA_SEMANA, 
        blank=True, 
        null=True,
        verbose_name="Dia da semana"
    )
    semanas_duracao = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(52)],
        verbose_name="Número de semanas",
        blank=True,
        null=True
    )

    def __str__(self):
        recorrencia = " (semanal)" if self.recorrente else ""
        return f"{self.nome} - {self.data_inicial} {self.hora}{recorrencia}"

    def get_data_completa(self):
        return f"{self.data_inicial} {self.hora}"

    def save(self, *args, **kwargs):
        # Se for recorrente, calcula o dia da semana automaticamente
        if self.recorrente and not self.dia_semana:
            self.dia_semana = str(self.data_inicial.weekday())  # 0=domingo, 1=segunda, etc.
        super().save(*args, **kwargs)

class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    posicao = models.CharField(max_length=50)

class Presenca(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)