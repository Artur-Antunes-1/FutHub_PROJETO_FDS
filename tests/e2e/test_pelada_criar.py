import pytest, datetime
from tests.e2e.pages.auth import AuthPage
from tests.e2e.pages.pelada import PeladaPage

@pytest.mark.asyncio
async def test_criar_pelada(live_server, page, create_user):
    create_user()
    auth = AuthPage(page, live_server.url)
    await auth.login("demo", "pass123")

    pp = PeladaPage(page, live_server.url)
    data = datetime.date.today().strftime("%Y-%m-%d")
    await pp.criar("Pelada Cypress", data, "18:00", "Arena 1", 8)

    await page.goto(f"{live_server.url}/peladas/")
    assert await page.is_visible("text=Pelada Cypress")
