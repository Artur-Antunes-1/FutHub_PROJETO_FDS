import pytest, datetime
from django.contrib.auth.models import User
from core.models import Pelada, Presenca, Jogador

@pytest.fixture
def create_user(db):
    def _make(username="demo", password="pass123", **extra):
        return User.objects.create_user(username=username, password=password, **extra)
    return _make

@pytest.fixture
def criar_pelada(db, create_user):
    def _make(dono=None, nome="Pelada E2E", data=None):
        dono = dono or create_user()
        data = data or datetime.date.today()
        pelada = Pelada.objects.create(
            nome=nome,
            data_inicial=data,
            hora="19:00",
            local="Quadra X",
            organizador=dono,
            limite_participantes=10
        )
        jogador = Jogador.objects.get(usuario=dono)
        Presenca.objects.create(pelada=pelada, jogador=jogador)
        return pelada
    return _make
