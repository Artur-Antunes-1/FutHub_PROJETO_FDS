import pytest
from tests.e2e.pages.auth   import AuthPage
from tests.e2e.pages.pelada import PeladaPage

@pytest.mark.asyncio
async def test_entrar_com_codigo(live_server, async_page, create_user, criar_pelada):
    user   = create_user()
    pelada = criar_pelada(dono=user)

    auth = AuthPage(async_page, live_server.url)
    await auth.login("demo", "pass123")

    pp = PeladaPage(async_page, live_server.url)
    await pp.entrar_com_codigo(pelada.codigo_acesso)

    # basta aparecer o título da pelada; não precisamos esperar troca de URL
    await async_page.wait_for_selector(f"text={pelada.nome}")
    # async_page.url já devolve str; não se usa await
    assert async_page.url.endswith(f"/peladas/{pelada.id}/")
