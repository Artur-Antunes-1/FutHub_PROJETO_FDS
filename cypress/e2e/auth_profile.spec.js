describe('Histórias 12 e 13 – Conta e Perfil', () => {
  it('12.1: Cadastro com dados válidos', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="email"]').type('novo@ex.com');
    cy.get('input[name="password1"]').type('senha123');
    cy.get('input[name="password2"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/accounts/profile/create/');
  });

  it('12.2: Senha com 6 caracteres', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="email"]').type('s6@ex.com');
    cy.get('input[name="password1"]').type('123456');
    cy.get('input[name="password2"]').type('123456');
    cy.get('button[type="submit"]').click();
    cy.contains('sucesso').should('exist');
  });

  it('12.3: E-mail duplicado — exibe erro', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="email"]').type('demo@ex.com');
    cy.get('input[name="password1"]').type('senha123');
    cy.get('input[name="password2"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.get('.errorlist').should('contain', 'E-mail já cadastrado');
  });

  it('13.1: Cadastro de perfil válido', () => {
    cy.login('demo', 'pass123');
    cy.visit('/accounts/profile/create/');
    cy.get('input[name="nome"]').type('Artur');
    cy.get('input[name="posicao"]').type('Meio');
    cy.get('input[name="foto"]').attachFile('avatar.png');
    cy.get('textarea[name="bio"]').type('Bio teste');
    cy.get('button[type="submit"]').click();
    cy.contains('Artur').should('exist');
  });

  it('13.2: Foto inválida — exibe erro', () => {
    cy.login('demo', 'pass123');
    cy.visit('/accounts/profile/create/');
    cy.get('input[name="foto"]').attachFile('arquivo.txt');
    cy.get('button[type="submit"]').click();
    cy.get('.errorlist').should('contain', 'Formato de imagem inválido');
  });

  it('13.3: Nome curto — exibe erro', () => {
    cy.login('demo', 'pass123');
    cy.visit('/accounts/profile/create/');
    cy.get('input[name="nome"]').type('Al');
    cy.get('input[name="posicao"]').type('Atacante');
    cy.get('button[type="submit"]').click();
    cy.get('.errorlist').should('contain', 'Mínimo de 3 caracteres');
  });
});
