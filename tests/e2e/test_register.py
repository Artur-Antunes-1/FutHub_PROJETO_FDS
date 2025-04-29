import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_register_flow(live_server, page):
    auth = AuthPage(page, live_server.url)
    await auth.register("novo_user", "segredo123")
    await page.wait_for_url("**/home")
    assert await page.is_visible("text=Bem-vindo")
