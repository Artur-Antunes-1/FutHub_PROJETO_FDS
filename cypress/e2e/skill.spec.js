describe('História 3 – Atribuir nível de habilidade', () => {
  const user = { username: 'demo', password: 'pass123' };
  const playerId = 'jogador-id-valido'; // ajuste conforme seu setup

  beforeEach(() => {
    cy.login(user.username, user.password);
  });

  it('Cenário 1: Atribuição válida (1–5)', () => {
    cy.setSkill(playerId, 4);
    cy.get('.nivel-display').should('contain', '4');
  });

  it('Cenário 2: Atualização de nível existente', () => {
    cy.setSkill(playerId, 2);
    cy.get('.nivel-display').should('contain', '2');
  });

  it('Cenário 3: Visualização de níveis', () => {
    cy.visit('/jogadores/');
    cy.get(`.jogador-${playerId} .nivel-display`).should('exist');
  });

  it('Cenário 4: Usuário comum não pode editar — exibe erro', () => {
    // usar outro usuário sem permissão
    cy.login('usuario-comum', 'senha123');
    cy.visit(`/jogadores/${playerId}/editar-habilidade/`);
    cy.get('.errorlist').should('contain', 'Permissão negada');
  });

  it('Cenário 5: Nível fora da faixa — exibe erro', () => {
    cy.setSkill(playerId, 6);
    cy.get('.errorlist').should('contain', 'Valor deve estar entre 1 e 5');
  });
});
