"""
Fixtures compartilhadas pelos testes E2E.

Notas
-----
▪ Definimos DJANGO_ALLOW_ASYNC_UNSAFE = true para poder usar a ORM síncrona
  dentro de funções async sem levantar `SynchronousOnlyOperation`.
▪ Criamos um fixture `async_page` que fornece o Page assíncrono do Playwright
  (compatível com as chamadas `await page.*` já usadas nos testes).
"""

import os, datetime, asyncio, pytest
from django.contrib.auth.models import User
from core.models import Pelada, Presenca, Jogador
from playwright.async_api import async_playwright

# --- Django: permitir ORM síncrona em contexto async --------------------------
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# --- loop do pytest-asyncio (escopo session) ----------------------------------
@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:          # noqa: D401
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ----------------------------------------------------------------------------- 
# 1) utilitário para criar usuários                                             #
# ----------------------------------------------------------------------------- 
@pytest.fixture
def create_user(db):
    """Cria um usuário rapidamente (`pass123` por padrão)."""
    def _make(username="demo", password="pass123", **extra):
        return User.objects.create_user(username=username,
                                        password=password,
                                        **extra)
    return _make

# ----------------------------------------------------------------------------- 
# 2) utilitário para criar peladas de teste                                     #
# ----------------------------------------------------------------------------- 
@pytest.fixture
def criar_pelada(db, create_user):
    """Cria uma pelada + presença do organizador."""
    def _make(*, dono=None, nome="Pelada E2E", data=None, limite=10):
        dono  = dono or create_user()
        data  = data or datetime.date.today()
        pelada = Pelada.objects.create(
            nome             = nome,
            data_inicial     = data,
            hora             = "19:00",
            local            = "Quadra X",
            organizador      = dono,
            limite_participantes = limite,
        )
        jogador = Jogador.objects.get(usuario=dono)
        Presenca.objects.create(pelada=pelada, jogador=jogador)
        return pelada
    return _make

# ----------------------------------------------------------------------------- 
# 3) página assíncrona do Playwright                                            #
# ----------------------------------------------------------------------------- 
@pytest.fixture
async def async_page():
    async with async_playwright() as p:
        browser  = await p.chromium.launch(headless=True)
        context  = await browser.new_context()
        page     = await context.new_page()
        yield page
        await context.close()
        await browser.close()
