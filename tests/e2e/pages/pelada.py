class PeladaPage:
    def __init__(self, page, base_url):
        self.p   = page
        self.base = base_url

    async def criar(self, nome, data, hora, local, limite):
        await self.p.goto(f"{self.base}/peladas/criar/")
        await self.p.fill('input[name="nome"]', nome)
        await self.p.fill('input[name="data_inicial"]', data)
        await self.p.fill('input[name="hora"]', hora)
        await self.p.fill('input[name="local"]', local)
        await self.p.fill('input[name="limite_participantes"]', str(limite))
        await self.p.click('button[type="submit"]')

     # ------------ NOVO ------------ #
    async def entrar_com_codigo(self, codigo):
        """Fluxo usado pelos testes para entrar numa pelada via código UUID."""
        await self.p.goto(f"{self.base}/peladas/entrar-com-codigo/")
        await self.p.fill('input[name=\"codigo_acesso\"]', str(codigo))
        await self.p.click('button[type=\"submit\"]')

    # Alias para compatibilidade, caso em algum lugar ainda use o nome antigo.
    async def entrar_codigo(self, codigo):
        await self.entrar_com_codigo(codigo)
