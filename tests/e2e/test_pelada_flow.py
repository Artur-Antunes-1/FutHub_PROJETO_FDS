import pytest, datetime
from tests.e2e.pages.auth import LoginPage
from tests.e2e.pages.pelada import PeladaPage

@pytest.mark.asyncio
async def test_criar_e_listar_pelada(live_server, page, create_user):
    create_user()
    # login
    lp = LoginPage(page, live_server.url)
    await lp.goto()
    await lp.login("demo", "pass123")

    # criar pelada
    pp = PeladaPage(page, live_server.url)
    data = datetime.date.today().strftime("%Y-%m-%d")
    await pp.criar("Pelada E2E", data, "19:00", "Quadra Central", 10)

    # lista deve conter
    await page.goto(f"{live_server.url}/peladas/")
    assert await page.is_visible("text=Pelada E2E")
