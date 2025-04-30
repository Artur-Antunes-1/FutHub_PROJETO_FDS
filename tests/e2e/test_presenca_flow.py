import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_confirmar_cancelar_presenca(live_server, async_page, create_user, criar_pelada):
    dono   = create_user()
    pelada = criar_pelada(dono=dono)

    auth = AuthPage(async_page, live_server.url)
    await auth.login("demo", "pass123")

    # confirma
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/presenca/")
    await async_page.wait_for_selector("text=Confirmado")

    # cancela
    await async_page.goto(f"{live_server.url}/peladas/{pelada.id}/cancelar/")
    await async_page.wait_for_selector("text=Confirmar Presença")   # botão voltou
    assert await async_page.is_visible("text=Confirmar Presença")
