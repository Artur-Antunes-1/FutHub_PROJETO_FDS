class AuthPage:
    def __init__(self, page, base_url):
        self.p        = page
        self.login_url = f"{base_url}/accounts/login/"
        self.reg_url   = f"{base_url}/accounts/register/"

    # todas as chamadas Playwright já são awaitables porque usaremos async_page
    async def login(self, user, pwd):
        await self.p.goto(self.login_url)
        await self.p.fill('input[name="username"]', user)
        await self.p.fill('input[name="password"]', pwd)
        await self.p.click('button[type="submit"]')

    async def register(self, user, pwd):
        await self.p.goto(self.reg_url)
        await self.p.fill('input[name="username"]', user)
        await self.p.fill('input[name="password1"]', pwd)
        await self.p.fill('input[name="password2"]', pwd)
        await self.p.click('button[type="submit"]')
