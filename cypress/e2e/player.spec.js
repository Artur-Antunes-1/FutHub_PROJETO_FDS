describe('História 2 – Adicionar jogadores', () => {
  const user = { username: 'demo', password: 'pass123' };
  const peladaId = 'test-pelada-id'; // ajuste para um ID válido no seu setup

  beforeEach(() => {
    cy.login(user.username, user.password);
  });

  it('Cenário 1: Cadastro bem-sucedido', () => {
    cy.createPlayer({
      nome: 'Jogador A',
      email: 'a@ex.com',
      posicao: 'Atacante',
      peladaId
    });
    cy.contains('Jogador A').should('exist');
  });

  it('Cenário 2: E-mail único', () => {
    cy.createPlayer({
      nome: 'Jogador B',
      email: 'b@ex.com',
      posicao: 'Meio',
      peladaId
    });
    cy.contains('b@ex.com').should('exist');
  });

  it('Cenário 3: Associar jogador existente', () => {
    // assume que 'Jogador A' já existe
    cy.createPlayer({
      nome: 'Jogador A',
      email: 'a@ex.com',
      posicao: 'Atacante',
      peladaId
    });
    cy.contains('Jogador A').should('have.length', 1);
  });

  it('Cenário 4: E-mail duplicado — exibe erro', () => {
    cy.createPlayer({
      nome: 'Jogador C',
      email: 'a@ex.com',
      posicao: 'Zagueiro',
      peladaId
    });
    cy.get('.errorlist').should('contain', 'E-mail já cadastrado');
  });

  it('Cenário 5: Posição em branco — exibe erro', () => {
    cy.createPlayer({
      nome: 'Jogador D',
      email: 'd@ex.com',
      posicao: '',
      peladaId
    });
    cy.get('.errorlist').should('contain', 'Este campo é obrigatório');
  });
});
