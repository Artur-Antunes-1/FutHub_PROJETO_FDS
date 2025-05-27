describe('Fluxo completo – Perfil, Pelada, Presença, Gerenciar e Ranking', () => {
  const user = { username: 'player1', password: 'senha123' };

  before(() => {
    cy.deleteUsers();
  });

  it('Configura perfil, cria pelada, confirma presença, gerencia estrelas e verifica ranking', () => {
    // 1) Registro e (re)login
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(user.username);
    cy.get('input[name="password1"]').type(user.password);
    cy.get('input[name="password2"]').type(user.password);
    cy.get('button[type="submit"]').click();
    // Garante que está logado; se preciso:
    cy.login(user.username, user.password);

    // 2) Ajusta perfil
    cy.visit('/perfil');
    cy.get('input[name="nome"]').clear().type('Jogador X');
    cy.get('select#id_posicao').select('Atacante');
    cy.get('select#id_perna_boa').select('Esquerda');
    cy.contains('button', 'Salvar perfil').click();

    // 3) Cria uma pelada
    cy.createPelada({
      nome:   'Pelada Full Flow',
      data:   '25/06/2025',
      hora:   '20:00',
      local:  'Quadra Central',
      limite: 5
    });
    cy.url().should('match', /\/peladas\/\d+\/$/);

    // 4) Confirma presença
    cy.contains('button', 'Confirmar Presença').click();
    cy.contains('Presença confirmada!').should('be.visible');

    // 5) Gerencia estrelas
    cy.contains('Gerenciar').click();
    cy.url().should('include', '/gerenciar/');
    cy.get('table tbody tr').first().within(() => {
      cy.get('select').first().select('4 estrelas');
    });
    cy.contains('Salvar Níveis').click();
    cy.contains('Voltar').click();
    cy.contains('Níveis de habilidade atualizados.').should('be.visible');

    // 6) Abre ranking de habilidade
    cy.contains('Ranking de Habilidade').click();
    cy.url().should('include', '/ranking/');

    // 7) Verifica no ranking
    cy.get('table tbody tr').first().within(() => {
      cy.contains(user.username).should('exist');
      cy.contains('Atacante').should('exist');
      cy.contains('Esquerda').should('exist');
      cy.get('svg.star-filled, .star.filled').should('have.length', 4);
    });
  });
});
