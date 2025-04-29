class AuthPage:
    def __init__(self, page, base):
        self.p  = page
        self.url_reg = f"{base}/accounts/register/"
        self.url_log = f"{base}/accounts/login/"

    async def register(self, user, pwd):
        await self.p.goto(self.url_reg)
        await self.p.fill('input[name="username"]', user)
        await self.p.fill('input[name="password1"]', pwd)
        await self.p.fill('input[name="password2"]', pwd)
        await self.p.click('button[type="submit"]')

    async def login(self, user, pwd):
        await self.p.goto(self.url_log)
        await self.p.fill('input[name="username"]', user)
        await self.p.fill('input[name="password"]', pwd)
        await self.p.click('button[type="submit"]')
