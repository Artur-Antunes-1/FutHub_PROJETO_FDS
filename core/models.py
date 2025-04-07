from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

def gerar_uuid():
    return uuid.uuid4()

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
    data_inicial = models.DateField()
    hora = models.TimeField(default='18:00:00')
    local = models.CharField(max_length=100)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)

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

    codigo_acesso = models.UUIDField(default=gerar_uuid, editable=False, unique=True)

    def __str__(self):
        recorrencia = " (semanal)" if self.recorrente else ""
        return f"{self.nome} - {self.data_inicial} {self.hora}{recorrencia}"

    def get_data_completa(self):
        return f"{self.data_inicial} {self.hora}"

    def save(self, *args, **kwargs):
        if self.recorrente and not self.dia_semana:
            self.dia_semana = str(self.data_inicial.weekday())
        if not self.codigo_acesso:
            self.codigo_acesso = gerar_uuid()
        super().save(*args, **kwargs)

class Jogador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jogador')
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    posicao = models.CharField(max_length=50, blank=True)
    peladas = models.ManyToManyField(Pelada, through='Presenca', related_name='jogadores')

    def __str__(self):
        return self.nome

class Presenca(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def criar_jogador_automatico(sender, instance, created, **kwargs):
    if created:
        Jogador.objects.get_or_create(
            usuario=instance,
            email=instance.email,
            defaults={'nome': instance.username}
        )
