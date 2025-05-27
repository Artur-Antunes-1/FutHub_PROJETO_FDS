describe('Fluxo de Presença – confirmar e cancelar presença', () => {
  const user = { username: 'demo', password: 'pass123' };

  beforeEach(() => {
    // Limpa usuários, cadastra e loga
    cy.deleteUsers();
    cy.login(user.username, user.password);

    // Cria uma pelada com capacidade de 10
    cy.createPelada({
      nome:   'Pelada Teste',
      data:   '15/06/2025',
      hora:   '19:00',
      local:  'Quadra Teste',
      limite: 10
    });

    // Após criar, já estamos na página de detalhes da pelada
    cy.url().should('match', /\/peladas\/\d+\/$/);
  });

  it('Confirma presença e exibe feedback visual', () => {
    // 1) Clica em "Confirmar Presença"
    cy.contains('button', 'Confirmar Presença').click();

    // 2) Exibe alerta de sucesso
    cy.contains('Presença confirmada!')
      .should('be.visible');

    // 3) Painel de participantes mostra 1 confirmado
    cy.contains('Confirmados:')
      .should('contain.text', '1')
      .and('contain.text', '/ 10');

    // 4) Botão muda para "Cancelar Presença"
    cy.contains('button', 'Cancelar Presença')
      .should('be.visible');
  });

  it('Cancela presença e exibe feedback visual', () => {
    // Primeiro confirme para depois cancelar
    cy.contains('button', 'Confirmar Presença').click();
    cy.contains('Presença confirmada!').should('be.visible');

    // 1) Clica em "Cancelar Presença"
    cy.contains('button', 'Cancelar Presença').click();

    // 2) Exibe alerta de cancelamento
    cy.contains('Presença cancelada.')
      .should('be.visible');

    // 3) Painel de participantes volta a mostrar 0 confirmados
    cy.contains('Confirmados:')
      .should('contain.text', '0')
      .and('contain.text', '/ 10');

    // 4) Botão volta a ser "Confirmar Presença"
    cy.contains('button', 'Confirmar Presença')
      .should('be.visible');
  });
});
