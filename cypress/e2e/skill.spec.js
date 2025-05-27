describe('História 3 – Gerenciar nível de habilidade', () => {
  const admin = { username: 'admin01', password: 'senhaAdmin' };

  beforeEach(() => {
    // 1) Limpa tudo
    cy.deleteUsers();

    // 2) Registra o admin
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(admin.username);
    cy.get('input[name="password1"]').type(admin.password);
    cy.get('input[name="password2"]').type(admin.password);
    cy.get('button[type="submit"]').click();

    // 3) Faz login (caso o register não logue automaticamente)
    cy.visit('/accounts/login/');
    cy.get('input[name="username"]').type(admin.username);
    cy.get('input[name="password"]').type(admin.password);
    cy.get('button[type="submit"]').click();

    // 4) Cria a pelada de teste
    cy.createPelada({
      nome:   'Pelada Ranking',
      data:   '20/06/2025',
      hora:   '21:00',
      local:  'Quadra Principal',
      limite: 5
    });

    // 5) Garante que chegou na página de detalhes
    cy.url().should('match', /\/peladas\/\d+\/$/);
  });

  it('Admin altera nível de estrela e vê ranking atualizado', () => {
    // 6) Clica em "Gerenciar" (mesmo com emoji)
    cy.contains('Gerenciar').click();

    // 7) Confirma rota de gerenciamento
    cy.url().should('match', /\/peladas\/\d+\/gerenciar\/$/);

    // 8) Seleciona "5 estrelas" para o primeiro jogador
    cy.get('table tbody tr').first().within(() => {
    // pega o primeiro <select> que aparecer na linha
    cy.get('select')
    .first()
    .should('be.visible')
    .select('5 estrelas');
 });

    // 9) Clica em "Salvar Níveis" e depois em "Voltar"
   cy.contains('Salvar Níveis').click();
   cy.contains('button, a', 'Voltar').click();

    // 10) Volta à página de detalhes
    cy.url().should('match', /\/peladas\/\d+\/$/);

    // 11) Espera mensagem de confirmação de níveis atualizados
    cy.contains('Níveis de habilidade atualizados.')
    .should('be.visible');
    });
  });
