class LoginPage:
    def __init__(self, page, base):
        self.page = page
        self.url  = f"{base}/accounts/login/"

    async def goto(self):
        await self.page.goto(self.url)

    async def login(self, user, pwd):
        await self.page.fill('input[name="username"]', user)
        await self.page.fill('input[name="password"]', pwd)
        await self.page.click('button[type="submit"]')
