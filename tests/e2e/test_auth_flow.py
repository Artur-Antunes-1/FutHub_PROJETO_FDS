import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_login(live_server, async_page, create_user):
    create_user()
    auth = AuthPage(async_page, live_server.url)
    await auth.login("demo", "pass123")
    await async_page.wait_for_url("**/")
    assert await async_page.is_visible("text=Bem-vindo")
