import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_perfil_atualiza_e_exibe(live_server, async_page, create_user, criar_pelada):
    # 1. Cria usuário e pelada para aparecer na lista
    user = create_user("profileuser", "pass123")
    pelada = criar_pelada(dono=user, nome="Pelada Perfil Test")

    # 2. Login
    auth = AuthPage(async_page, live_server.url)
    await auth.login("profileuser", "pass123")

    # 3. Acessa página de perfil
    await async_page.goto(f"{live_server.url}/perfil/")
    await async_page.wait_for_selector('#id_nome')

    # 4. Atualiza campos: nome, posição e perna boa
    await async_page.fill('input[name="nome"]', "Test User")
    await async_page.select_option('select[name="posicao"]', "ATA")
    await async_page.select_option('select[name="perna_boa"]', "A")
    await async_page.click('button[type="submit"]')

    # 5. Aguarda o redirecionamento e confere se o nome foi atualizado
    await async_page.wait_for_selector('input[name="nome"][value="Test User"]')

    # 6. Garante que os campos mantêm os valores salvos
    assert await async_page.input_value('input[name="nome"]') == "Test User"
    assert await async_page.input_value('select[name="posicao"]') == "ATA"
    assert await async_page.input_value('select[name="perna_boa"]') == "A"

    # 7. Verifica lista de peladas que participa
    assert await async_page.is_visible("text=Pelada Perfil Test")
