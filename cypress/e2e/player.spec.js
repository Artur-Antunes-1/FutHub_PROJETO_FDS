describe('Fluxo: Usuário 1 cria a pelada e Usuário 2 entra com o código', () => {
  const creator = { username: 'user1', password: 'pass123' };
  const guest   = { username: 'user2', password: 'pass456' };
  let codigo;

  before(() => {
    cy.deleteUsers();
  });

  it('Usuário 1 registra e cria a pelada', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(creator.username);
    cy.get('input[name="password1"]').type(creator.password);
    cy.get('input[name="password2"]').type(creator.password);
    cy.get('button[type="submit"]').click();

    cy.login('user1', 'pass123');
    cy.createPelada({
    nome:   'Pelada Exemplo',
    data:   '27/05/2025',
    hora:   '20:30',
    local:  'Quadra da Esquina',
    limite: 12
  });
  cy.contains('Pelada Exemplo').should('exist');


    cy.contains('Código de Acesso')
      .parent()
      .find('p')
      .invoke('text')
      .then(text => {
        codigo = text.trim();
        expect(codigo).to.match(/[0-9a-fA-F\-]{36}/);
      });
  });

  it('Usuário 2 registra e entra na pelada com o código', () => {
    cy.visit('/accounts/logout/');

    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(guest.username);
    cy.get('input[name="password1"]').type(guest.password);
    cy.get('input[name="password2"]').type(guest.password);
    cy.get('button[type="submit"]').click();

    cy.login('user2', 'pass456');

    cy.enterPeladaByCode(codigo);

    cy.url().should('match', /\/peladas\/\d+\/$/);
    cy.contains(guest.username).should('be.visible');
  });
});

it('Código inválido — exibe mensagem de erro', () => {
  // já deve estar logado como qualquer usuário válido
  cy.login('user2', 'pass456');

  // navega direto para a tela de entrada por código
  cy.visit('/peladas/entrar-com-codigo/');

  // digita um UUID inexistente
  cy.get('input[type="text"]')
    .clear()
    .type('00000000-0000-0000-0000-000000000000');

  // tenta entrar
  cy.contains('button', 'Entrar').click();

  // URL permanece na tela de entrada por código
   cy.url().should('include', '/peladas/entrar-com-codigo/');

  // validação visual de erro (pode ser .error-message ou .errorlist)
   cy.get('.error-message, .errorlist')
     .should('be.visible')
     .and($els => {
       expect($els.length, 'número de elementos de erro').to.be.greaterThan(0);
     });

  // verifica a mensagem de erro na página
  cy.get('.error-message').should('be.visible');

});
