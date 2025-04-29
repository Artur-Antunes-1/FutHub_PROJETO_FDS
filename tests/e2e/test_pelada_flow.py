import pytest, datetime as dt
from tests.e2e.pages.auth   import AuthPage
from tests.e2e.pages.pelada import PeladaPage

@pytest.mark.asyncio
async def test_criar_e_listar_pelada(live_server, async_page, create_user):
    create_user()
    auth = AuthPage(async_page, live_server.url)
    await auth.login("demo", "pass123")

    pp   = PeladaPage(async_page, live_server.url)
    data = dt.date.today().strftime("%Y-%m-%d")
    await pp.criar("Pelada E2E", data, "19:00", "Quadra Central", 10)

    await async_page.goto(f"{live_server.url}/peladas/")
    assert await async_page.is_visible("text=Pelada E2E")
