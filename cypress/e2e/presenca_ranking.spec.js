describe('Histórias 5, 7 e 11 – Presença, Ranking e Admin', () => {
  const user = { username: 'demo', password: 'pass123' };

  beforeEach(() => {
    cy.login(user.username, user.password);
  });

  // 5. Registrar presença
  it('5.1: Jogador confirma presença', () => {
    cy.visit('/peladas/minhas/');
    cy.contains('Confirmar presença').click();
    cy.contains('Confirmado').should('exist');
  });
  it('5.2: Jogador recusa presença', () => {
    cy.visit('/peladas/minhas/');
    cy.contains('Recusar presença').click();
    cy.contains('Ausente').should('exist');
  });
  it('5.3: Não cadastrado — exibe erro', () => {
    cy.visit(`/peladas/foradaLista/confirmar/`);
    cy.get('.errorlist').should('contain', 'Não autorizado');
  });
  it('5.4: Organizador vê lista', () => {
    cy.visit(`/peladas/minhas/presenca/`);
    cy.get('.confirmados').should('exist');
    cy.get('.ausentes').should('exist');
  });

  // 7. Ranking
  it('7.1: Geração de ranking', () => {
    cy.visit('/ranking/');
    cy.get('.ranking-row').its('length').should('be.gt', 0);
  });
  it('7.2: Atualização automática', () => {
    // após registrar presença ou resultado
    cy.visit('/ranking/').contains('demo').should('exist');
  });
  it('7.3: Filtro por temporada', () => {
    cy.get('select#temporada').select('2025');
    cy.get('.ranking-row').should('exist');
  });
  it('7.4: Critério de desempate', () => {
    // simula empate e verifica desempate
    cy.visit('/ranking/');
    cy.get('.ranking-row.tie').first().should('have.class', 'break-rule');
  });

  // 11. Admin – edição/exclusão
  it('11.1: Editar jogador (admin)', () => {
    cy.visit('/admin/jogador/demo/editar/');
    cy.get('input[name="posicao"]').clear().type('Goleiro');
    cy.get('button[type="submit"]').click();
    cy.contains('Goleiro').should('exist');
  });
  it('11.2: Excluir jogador (admin)', () => {
    cy.visit('/admin/jogador/demo/excluir/');
    cy.get('button.confirm').click();
    cy.contains('demo').should('not.exist');
  });
});
