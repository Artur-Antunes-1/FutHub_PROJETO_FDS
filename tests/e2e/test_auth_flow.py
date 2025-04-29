import pytest
from tests.e2e.pages.auth import LoginPage

@pytest.mark.asyncio
async def test_login_workflow(live_server, page, create_user):
    create_user()
    lp = LoginPage(page, live_server.url)
    await lp.goto()
    await lp.login("demo", "pass123")
    await page.wait_for_url("**/home")
    assert await page.is_visible("text=Bem-vindo")  # ajuste texto conforme template
