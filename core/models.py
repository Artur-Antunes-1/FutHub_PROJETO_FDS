
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.contrib.auth import get_user_model

def gerar_uuid():
    """Gera um UUID v4; usado como código de acesso para a pelada."""
    return uuid.uuid4()

class Pelada(models.Model):
    """Representa um jogo de futebol entre amigos."""
    codigo_acesso = models.UUIDField(default=gerar_uuid, unique=True, editable=False)
    nome = models.CharField(max_length=120)
    data_inicial = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=120)
    recorrente = models.BooleanField(default=False)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peladas_criadas')
    limite_participantes = models.IntegerField(default=20)
    
    class Meta:
        ordering = ['-data_inicial', 'hora']

    def __str__(self):
        return f"{self.nome} ({self.data_inicial.strftime('%d/%m/%Y')})"

    @property
    def participantes(self):
        """
        Retorna um QuerySet de Jogador ligados a esta pelada,
        incluído o organizador (é criado no momento da pelada).
        """
        from .models import Jogador          # import local para evitar ciclos
        return Jogador.objects.filter(presenca__pelada=self)

# core/models.py

class Jogador(models.Model):
    POSICAO_CHOICES = [
        ('GOL', 'Goleiro'),
        ('DEF', 'Defensor'),
        ('MC', 'Meio Campista'),
        ('ATA', 'Atacante'),
    ]
    PERNA_CHOICES = [
        ('D', 'Direita'),
        ('E', 'Esquerda'),
        ('A', 'Ambidestro'),
    ]
    usuario      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jogador')
    nome         = models.CharField(max_length=150)
    posicao      = models.CharField(max_length=3, choices=POSICAO_CHOICES, blank=True)
    perna_boa = models.CharField(max_length=1, choices=PERNA_CHOICES, default='D')

    def __str__(self):
        return self.nome

class Presenca(models.Model):
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    nivel_habilidade = models.IntegerField(
        default=3,
        choices=[(i, f"{i} estrela{'s' if i>1 else ''}") for i in range(1,6)],
        verbose_name='Nível de Habilidade'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pelada', 'jogador')
        ordering = ['pelada', 'jogador']

    def __str__(self):
        status = '✅' if self.confirmado else '⏳'
        return f"{self.jogador} em {self.pelada} {status}"

# Cria automaticamente um Jogador assim que o User é criado
@receiver(post_save, sender=User)
def criar_jogador_automatico(sender, instance, created, **kwargs):
    if created:
        Jogador.objects.create(
            usuario=instance,
            nome=instance.username,
            email=instance.email
        )

User = get_user_model()

class Sorteio(models.Model):
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE, related_name='sorteios')
    criado_em = models.DateTimeField(auto_now_add=True)

class SorteioTime(models.Model):
    sorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE, related_name='times')
    nome = models.CharField(max_length=50)
    total_estrelas = models.PositiveIntegerField()
    vagas = models.PositiveIntegerField()

class SorteioJogador(models.Model):
    time = models.ForeignKey(SorteioTime, on_delete=models.CASCADE, related_name='jogadores')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    nivel_habilidade = models.PositiveIntegerField()