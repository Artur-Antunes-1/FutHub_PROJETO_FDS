class PeladaPage:
    def __init__(self, page, base):
        self.page = page
        self.base = base

    async def criar(self, nome, data, hora, local, limite):
        await self.page.goto(f"{self.base}/peladas/criar/")
        await self.page.fill('input[name="nome"]', nome)
        await self.page.fill('input[name="data_inicial"]', data)
        await self.page.fill('input[name="hora"]', hora)
        await self.page.fill('input[name="local"]', local)
        await self.page.fill('input[name="limite_participantes"]', str(limite))
        await self.page.click('button[type="submit"]')
