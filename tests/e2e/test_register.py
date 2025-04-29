import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_register(live_server, async_page):
    auth = AuthPage(async_page, live_server.url)
    await auth.register("novo_user", "segredo123")
    await async_page.wait_for_url("**/")          # a home é “/”
    assert await async_page.is_visible("text=Bem-vindo")
