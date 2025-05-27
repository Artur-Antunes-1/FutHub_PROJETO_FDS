// cypress/e2e/sortear_times_8.spec.js

describe('História 5 ajustada – Sortear Times com 8 jogadores', () => {
  const ts = Date.now();
  const creator = { username: `creator_${ts}`, password: 'senhaCriador' };
  const players = Array.from({ length: 7 }, (_, i) => ({
    username: `player${i + 1}_${ts}`,
    password: `senha${i + 1}`
  }));
  let codigo;
  let peladaId;

  before(() => {
    cy.deleteUsers();

    // registra creator (faz login automático)
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(creator.username);
    cy.get('input[name="password1"]').type(creator.password);
    cy.get('input[name="password2"]').type(creator.password);
    cy.get('button[type="submit"]').click();

    // cria pelada para 8
    cy.createPelada({
      nome:   'Pelada 8 jogadores',
      data:   '15/07/2025',
      hora:   '20:00',
      local:  'Quadra Pequena',
      limite: 8
    });

    // captura ID da pelada da URL
    cy.url().should('match', /\/peladas\/(\d+)\//).then(url => {
      peladaId = url.match(/\/peladas\/(\d+)\//)[1];
    });

    // captura código de acesso
    cy.contains('Código de Acesso')
      .parent()
      .find('p')
      .invoke('text')
      .then(txt => {
        codigo = txt.trim();
        expect(codigo).to.match(/[0-9a-fA-F\-]{36}/);
      });
  });

  it('Registra 7 players, entra com código e confirma presença (total 8)', () => {
    players.forEach(p => {
      // registra cada jogador (login automático)
      cy.visit('/accounts/register/');
      cy.get('input[name="username"]').type(p.username);
      cy.get('input[name="password1"]').type(p.password);
      cy.get('input[name="password2"]').type(p.password);
      cy.get('button[type="submit"]').click();

      // entra na pelada e confirma
      cy.enterPeladaByCode(codigo);
      cy.contains('button', 'Confirmar Presença').click();
      cy.contains('Presença confirmada!').should('be.visible');

      // logout
      cy.visit('/accounts/logout/');
    });

    // reloga creator e visita detalhes
    cy.visit('/accounts/login/');
    cy.get('input[name="username"]').type(creator.username);
    cy.get('input[name="password"]').type(creator.password);
    cy.get('button[type="submit"]').click();
    cy.visit(`/peladas/${peladaId}/`);

    // verifica 8/8 confirmados
    cy.contains('button', 'Confirmar Presença').click();
    cy.contains('Presença confirmada!').should('be.visible');
    cy.contains('Confirmados: 8 / 8').should('be.visible');
  });

  it('Creator atribui níveis (1,5,2,2,3,3,4,4) e sorteia 4 times de 2', () => {
    // reloga creator e visita detalhes
    cy.visit('/accounts/login/');
    cy.get('input[name="username"]').type(creator.username);
    cy.get('input[name="password"]').type(creator.password);
    cy.get('button[type="submit"]').click();
    
    // garante que está na página de detalhes
    cy.visit(`/peladas/${peladaId}/`);

     // clica em Gerenciar
  cy.contains('Gerenciar').click();
  cy.url().should('include', `/peladas/${peladaId}/gerenciar/`);

  // distribui níveis exatos
  const níveis = [1,5,2,2,3,3,4,4];
  cy.get('table tbody tr').each((row, idx) => {
    const level = níveis[idx];
    const label = `${level} estrela${level > 1 ? 's' : ''}`;
    cy.wrap(row)
      .find('select')
      .first()
      .select(label);
  });

  // salva e volta
  cy.contains('Salvar Níveis').click();
  cy.contains('Voltar').click();
  cy.contains('Níveis de habilidade atualizados.').should('be.visible');

  // visita detalhes de novo
  cy.visit(`/peladas/${peladaId}/`);

  // sorteia times
  cy.contains('Sortear Times').click();
  cy.url().should('include', '/ver-sorteio/');

  // após sortear, volta para a pelada
  cy.contains('← Voltar para Pelada').click();
  cy.contains('Times sorteados e salvos!').should('be.visible');
  cy.url().should('include', `/peladas/${peladaId}/`);

  // botão "Ver Sorteio" deve aparecer
  cy.contains('Ver Sorteio').should('be.visible').click();

  // volta à página de sorteio
  cy.url().should('include', `/peladas/${peladaId}/ver-sorteio/`);
});
});