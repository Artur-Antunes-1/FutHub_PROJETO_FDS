"""
Smoke-test: fluxo completo de autenticação (registro + login + logout).
Roda rápido e serve como “sanity check” para o CI.
"""
import pytest
from tests.e2e.pages.auth import AuthPage

@pytest.mark.asyncio
async def test_login_flow(live_server, async_page):
    auth = AuthPage(async_page, live_server.url)

    # 1. registro
    await auth.register("user_flow", "pass123")
    await async_page.wait_for_url("**/")
    assert await async_page.is_visible("text=Bem-vindo")

    # 2. logout
    await async_page.goto(f"{live_server.url}/accounts/logout/")
    await async_page.wait_for_selector("text=Login")               # página de login reaparece

    # 3. login novamente
    await auth.login("user_flow", "pass123")
    await async_page.wait_for_url("**/")
    assert await async_page.is_visible("text=Bem-vindo")
