Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
        console.log(result.stdout); 
        if (result.stderr) {
            console.error(result.stderr);
        } else {
            console.log('Usuários excluídos com sucesso');
        }
    });
});

describe('Histórias 1 e 2 – Registro e Login', () => {
  const user = { username: 'demo', password: 'pass123' };

  it('1. Registro de usuário', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type(user.username);
    cy.get('input[name="password1"]').type(user.password);
    cy.get('input[name="password2"]').type(user.password);
    cy.get('button[type="submit"]').click();
    // cy.url().should('include', '/accounts/profile/');
  });

  it('2. Login de usuário existente', () => {
    cy.login(user.username, user.password);
    cy.url().should('eq', Cypress.config().baseUrl + '/');
    cy.contains(user.username).should('be.visible');
  });
});
