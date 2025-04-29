import pytest
from tests.e2e.pages.auth import AuthPage
from core.models import Presenca, Jogador


@pytest.mark.asyncio
async def test_sorteio_times(live_server, async_page, create_user, criar_pelada):
    # 1‒ cria pelada com organizador + limite
    dono   = create_user("organizador")
    pelada = criar_pelada(dono=dono, limite=8)

    # confirma o organizador
    pres_org = Presenca.objects.get(
        pelada=pelada, jogador__usuario__username="organizador"
    )
    pres_org.confirmado = True
    pres_org.save(update_fields=["confirmado"])

    # 2‒ cria e confirma mais 7 jogadores
    for i in range(1, 8):
        u = create_user(f"user{i}")
        jogador = Jogador.objects.get(usuario=u)
        Presenca.objects.create(
            pelada=pelada, jogador=jogador, confirmado=True
        )

    # 3‒ login e executa o sorteio
    auth = AuthPage(async_page, live_server.url)
    await auth.login("organizador", "pass123")

    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/sortear/")

    # 4‒ garante que ao menos o primeiro cartão apareceu
    await async_page.wait_for_selector("h3:has-text('Time 1')")
