class PeladaPage:
    def __init__(self, page, base):
        self.p, self.base = page, base

    async def criar(self, nome, data, hora, local, limite):
        await self.p.goto(f"{self.base}/peladas/criar/")
        await self.p.fill('input[name="nome"]', nome)
        await self.p.fill('input[name="data_inicial"]', data)
        await self.p.fill('input[name="hora"]', hora)
        await self.p.fill('input[name="local"]', local)
        await self.p.fill('input[name="limite_participantes"]', str(limite))
        await self.p.click('button[type="submit"]')

    async def entrar_com_codigo(self, codigo):
        await self.p.goto(f"{self.base}/peladas/entrar-com-codigo/")
        await self.p.fill('input[name="codigo_acesso"]', str(codigo))
        await self.p.click('button[type="submit"]')
