// LOGIN
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/accounts/login/');
  cy.get('input[name="username"]').type(username);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
});

// CRIAR PELADA
Cypress.Commands.add('createPelada', ({ nome, data, hora, local, limite }) => {
  // converte "D/M/YYYY" ou "DD/MM/YYYY" em ISO "YYYY-MM-DD"
  const [diaRaw, mesRaw, ano] = data.split('/');
  const dia = diaRaw.padStart(2, '0');
  const mes = mesRaw.padStart(2, '0');
  const iso = `${ano}-${mes}-${dia}`; // YYYY-MM-DD

  cy.visit('/peladas/criar/');

  // Nome
  cy.get('input[name="nome"]')
    .clear()
    .type(nome);

  // Data nativa
  cy.get('input[name="data_inicial"]')
    .clear()
    .type(iso)
    .blur();

  // Hora
  cy.get('input[name="hora"]')
    .clear()
    .type(hora);

  // Local
  cy.get('input[name="local"]')
    .clear()
    .type(local);

  // Limite de participantes
  cy.get('input[name="limite_participantes"]')
    .clear()
    .type(`${limite}`);

  // Salvar pelada
  cy.get('button[type="submit"]')
    .contains(/Salvar/i)
    .click();
});

// ENTRAR POR CÓDIGO
Cypress.Commands.add('enterPeladaByCode', (codigo) => {
  cy.visit('/peladas/entrar-com-codigo/');
  // captura o campo de texto (único input[type="text"] na página)
  cy.get('input[type="text"]')
    .clear()
    .type(codigo);
  cy.get('button[type="submit"]')
    .contains(/Entrar/i)
    .click();
});

// DELETE USERS (setup)
Cypress.Commands.add('deleteUsers', () => {
  return cy.exec('python delete_users.py', { failOnNonZeroExit: false });
});

// CRIAR JOGADOR
Cypress.Commands.add('createPlayer', ({ nome, email, posicao, peladaId }) => {
  cy.visit(`/peladas/${peladaId}/adicionar-jogador/`);
  cy.get('input[name="nome"]').clear().type(nome);
  cy.get('input[name="email"]').clear().type(email);

  // posição via <select>
  if (posicao) {
    cy.get('select[name="posicao"]')
      .should('be.visible')
      .select(posicao);
  }

  cy.get('button[type="submit"]')
    .click();
});

// ATRIBUIR HABILIDADE
Cypress.Commands.add('setSkill', (playerId, nivel) => {
  cy.visit(`/jogadores/${playerId}/editar-habilidade/`);
  cy.get('input[name="nivel"]')
    .clear()
    .type(`${nivel}`);
  cy.get('button[type="submit"]')
    .click();
});
