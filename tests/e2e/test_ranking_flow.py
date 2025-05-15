import pytest
from tests.e2e.pages.auth import AuthPage
from core.models import Jogador, Presenca

@pytest.mark.asyncio
async def test_ranking_exibe_posicao_e_perna(live_server, async_page, create_user, criar_pelada):
    # 1. Cria organizador e dois jogadores
    organizador = create_user("org_ranking", "pass123")
    u1 = create_user("jog1", "pass123")
    u2 = create_user("jog2", "pass123")

    # 2. Ajusta perfil dos jogadores
    j1 = Jogador.objects.get(usuario=u1)
    j1.posicao = "MC"
    j1.perna_boa = "D"
    j1.save()
    j2 = Jogador.objects.get(usuario=u2)
    j2.posicao = "ATA"
    j2.perna_boa = "E"
    j2.save()

    # 3. Cria pelada e confirma presença de ambos
    pelada = criar_pelada(dono=organizador, nome="Pelada Ranking Test")
    Presenca.objects.create(pelada=pelada, jogador=j1, confirmado=True, nivel_habilidade=3)
    Presenca.objects.create(pelada=pelada, jogador=j2, confirmado=True, nivel_habilidade=1)

    # 4. Login como organizador e acessa ranking
    auth = AuthPage(async_page, live_server.url)
    await auth.login("org_ranking", "pass123")
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/ranking/")
    await async_page.wait_for_selector("text=Ranking:")

    # 5. Verifica colunas e valores de Posição e Perna Boa
    assert await async_page.is_visible("text=Posição")
    assert await async_page.is_visible("text=Perna Boa")
    assert await async_page.is_visible("text=Meio Campista")
    assert await async_page.is_visible("text=Direita")
    assert await async_page.is_visible("text=Atacante")
    assert await async_page.is_visible("text=Esquerda")
