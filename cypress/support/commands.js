// LOGIN
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/accounts/login/');
  cy.get('input[name="username"]').type(username);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
});

// CRIAR PELADA
Cypress.Commands.add('createPelada', ({ nome, data, hora, local, limite }) => {
  cy.visit('/peladas/criar/');
  cy.get('input[name="nome"]').clear().type(nome);
  cy.get('input[name="data_inicial"]').clear().type(data);
  cy.get('input[name="hora"]').clear().type(hora);
  cy.get('input[name="local"]').clear().type(local);
  cy.get('input[name="limite_participantes"]').clear().type(`${limite}`);
  cy.get('button[type="submit"]').click();
});

// ENTRAR POR CÓDIGO
Cypress.Commands.add('enterWithCode', (codigo) => {
  cy.visit('/peladas/entrar-com-codigo/');
  cy.get('input[name="codigo_acesso"]').clear().type(codigo);
  cy.get('button[type="submit"]').click();
});

// CRIAR JOGADOR
Cypress.Commands.add('createPlayer', ({ nome, email, posicao, peladaId }) => {
  cy.visit(`/peladas/${peladaId}/adicionar-jogador/`);
  cy.get('input[name="nome"]').clear().type(nome);
  cy.get('input[name="email"]').clear().type(email);
  cy.get('input[name="posicao"]').clear().type(posicao);
  cy.get('button[type="submit"]').click();
});

// ATRIBUIR HABILIDADE
Cypress.Commands.add('setSkill', (playerId, nivel) => {
  cy.visit(`/jogadores/${playerId}/editar-habilidade/`);
  cy.get('input[name="nivel"]').clear().type(`${nivel}`);
  cy.get('button[type="submit"]').click();
});
