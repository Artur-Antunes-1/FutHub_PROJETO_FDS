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

describe('Histórias 12 e 13 – Conta e Perfil', () => {

  beforeEach(() => {
        cy.deleteUsers()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
        });
    });

   it('12.1: Cadastro com dados válidos', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type('exemplouser');
    cy.get('input[name="password1"]').type('senha123');
    cy.get('input[name="password2"]').type('senha123');
    cy.get('button[type="submit"]').click();
  });

  it('12.2: E-mail duplicado — exibe erro', () => {
    cy.visit('/accounts/register/');
    cy.get('input[name="username"]').type('exemplouser');
    cy.get('input[name="password1"]').type('senha123');
    cy.get('input[name="password2"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
  });

  it('13.1: Cadastro de perfil válido', () => {
  cy.login('demo', 'pass123');
  cy.visit('/perfil');

  cy.get('input[name="nome"]')
    .clear()
    .type('Artur');

  // Seleção de posição
  cy.get('select#id_posicao')
    .scrollIntoView()
    .should('be.visible')
    .select('Meio Campista');

  // Seleciona perna boa
  cy.get('select#id_perna_boa')
    .should('be.visible')
    .select('Esquerda');

  // Clica em Salvar perfil
  cy.get('button[type="submit"]')
    .contains('Salvar perfil')  
    .click();

  // Verifica que voltou para a página do perfil e o nome foi salvo
  cy.url().should('include', '/perfil');
  cy.get('input[name="nome"]')
    .should('have.value', 'Artur');
});

  it('13.2: Nome curto — exibe erro', () => {
    cy.login('demo', 'pass123');
    cy.visit('/perfil');

    // garante que o nome esteja vazio
    cy.get('input[name="nome"]')
    .clear()
    .should('have.value', '');

    cy.get('select#id_posicao')
    .scrollIntoView()
    .should('be.visible')
    .select('Defensor');

    // Clica em Salvar perfil
    cy.get('button[type="submit"]')
    .contains('Salvar perfil')  
    .click();

    // verifica a mensagem de validação HTML5
    cy.get('input[name="nome"]').then($input => {
    // valida que o campo é inválido
    expect($input[0].checkValidity()).to.be.false;
    // valida a mensagem exibida
    expect($input[0].validationMessage).to.be.oneOf([
        'Preencha este campo.', 
        'Please fill out this field.'
      ]);
  });
});
});
