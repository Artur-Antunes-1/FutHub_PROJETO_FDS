describe('História 4 – Editar dados da Pelada', () => {
  const user = { username: 'creator', password: 'senha123' };

  beforeEach(() => {
    // limpa tudo, registra e faz login
    cy.deleteUsers();
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(user.username);
    cy.get('input[name="password1"]').type(user.password);
    cy.get('input[name="password2"]').type(user.password);
    cy.get('button[type="submit"]').click();
    cy.login(user.username, user.password);

    // cria uma pelada original
    cy.createPelada({
      nome:   'Pelada Original',
      data:   '10/07/2025',
      hora:   '18:30',
      local:  'Quadra A',
      limite: 12
    });

    // confirma que estamos nos detalhes
    cy.url().should('match', /\/peladas\/\d+\/$/);
  });

  it('Cenário 1: Deixar nome em branco — exibe erro HTML5', () => {
    // abre tela de edição
    cy.contains('Editar').click();
    cy.url().should('include', '/editar/');

    // limpa o campo nome
    cy.get('input[name="nome"]')
      .clear()
      .should('have.value', '');

    // tenta submeter
    cy.get('button[type="submit"]').contains(/Salvar/i).click();

    // validação HTML5
    cy.get('input[name="nome"]').then($el => {
      expect($el[0].checkValidity()).to.be.false;
      expect($el[0].validationMessage).to.equal('Preencha este campo.');
    });
  });

  it('Cenário 2: Editar com sucesso e ver detalhes atualizados', () => {
    // abre tela de edição
    cy.contains('Editar').click();
    cy.url().should('include', '/editar/');

    // preenche novos dados
    cy.get('input[name="nome"]')
      .clear()
      .type('Pelada Editada');
    // altera data
    cy.get('input[name="data_inicial"]')
      .clear()
      .type('2025-08-15')
      .blur();
    // altera hora
    cy.get('input[name="hora"]')
      .clear()
      .type('20:45');
    // altera local e limite
    cy.get('input[name="local"]')
      .clear()
      .type('Quadra B');
    cy.get('input[name="limite_participantes"]')
      .clear()
      .type('16');

    // submete
    cy.get('button[type="submit"]').contains(/Salvar/i).click();

    // volta para detalhes e verifica
    cy.url().should('match', /\/peladas\/\d+\/$/);
    cy.contains('Pelada Editada').should('be.visible');
    cy.contains('15/08/2025').should('be.visible');
    cy.contains('20:45').should('be.visible');
    cy.contains('Quadra B').should('be.visible');
    cy.contains('Confirmados: 0 / 16').should('be.visible');
  });
});
