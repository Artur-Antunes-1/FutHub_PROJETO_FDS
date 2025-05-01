import pytest
from tests.e2e.pages.auth import AuthPage
from core.models import Presenca, Jogador

@pytest.mark.asyncio
async def test_atribuicao_nivel_valido(live_server, async_page, create_user, criar_pelada):
    # Setup: organizador e pelada com 2 jogadores confirmados
    organizador = create_user("org1", "pass123")
    pelada = criar_pelada(dono=organizador)
    # cria e confirma presença de 2 jogadores
    pres_list = []
    for i in range(2):
        u = create_user(f"user{i}", "pass123")
        j = Jogador.objects.get(usuario=u)
        pres = Presenca.objects.create(pelada=pelada, jogador=j, confirmado=True)
        pres_list.append(pres)

    # Login como organizador
    auth = AuthPage(async_page, live_server.url)
    await auth.login(organizador.username, "pass123")

    # Atribuir nível válido = 4 ao primeiro presenca
    pres = pres_list[0]
    # Navegar para gerenciamento de níveis
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/gerenciar/")
    # Selecionar nível no select correspondente e salvar
    await async_page.select_option(f'select[name="nivel_{pres.id}"]', "4")
    await async_page.click('button[name="salvar_niveis"]')

    # Verifica no banco de dados
    pres.refresh_from_db()
    assert pres.nivel_habilidade == 4

    # Verifica exibição de estrelas na página de detalhes
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/")
    # Deve haver ao menos uma estrela preenchida
    assert await async_page.is_visible(".star.filled")

@pytest.mark.asyncio
async def test_atualizacao_nivel_existente(live_server, async_page, create_user, criar_pelada):
    # Setup: organizador e pelada com 1 jogador já com nível definido
    organizador = create_user("org2", "pass123")
    pelada = criar_pelada(dono=organizador)
    u = create_user("jogador", "pass123")
    j = Jogador.objects.get(usuario=u)
    pres = Presenca.objects.create(pelada=pelada, jogador=j, confirmado=True)
    pres.nivel_habilidade = 2
    pres.save(update_fields=["nivel_habilidade"])

    # Login e navegação à gerência
    auth = AuthPage(async_page, live_server.url)
    await auth.login(organizador.username, "pass123")
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/gerenciar/")

    # Alterar nível para 5 e salvar
    await async_page.select_option(f'select[name="nivel_{pres.id}"]', "5")
    await async_page.click('button[name="salvar_niveis"]')

    # Valida atualização no DB e UI
    pres.refresh_from_db()
    assert pres.nivel_habilidade == 5
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/")
    # Verificar pelo número de estrelas preenchidas
    filled = await async_page.query_selector_all('.star.filled')
    assert len(filled) >= 5
