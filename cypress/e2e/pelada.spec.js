describe('História 1 – Criação de pelada', () => {
  const user = { username: 'demo', password: 'pass123' };

  beforeEach(() => {
    cy.login(user.username, user.password);
  });

  it('Cenário 1: criação bem‐sucedida', () => {
  cy.login('demo', 'pass123');
  cy.createPelada({
    nome:   'Pelada Exemplo',
    data:   '27/05/2025',
    hora:   '20:30',
    local:  'Quadra da Esquina',
    limite: 12
  });
  cy.contains('Pelada Exemplo').should('exist');
});

  it('Cenário 2: Data em formato válido', () => {
    cy.createPelada({
      nome: 'DataVálida',
      data: '7/04/2025',
      hora: '19:00',
      local: 'Quadra B',
      limite: 8
    });
    cy.contains('DataVálida').should('exist');
  });

  it('Cenário 3: Local com mais de 3 caracteres', () => {
    cy.createPelada({
      nome: 'LocalOK',
      data: '08/04/2025',
      hora: '18:00',
      local: 'ABCd',
      limite: 5
    });
    cy.contains('LocalOK').should('exist');
  });

  it('Cenário 4: Nome em branco — exibe erro nativo “Preencha este campo.”', () => {
  cy.login('demo', 'pass123');
  cy.visit('/peladas/criar/');

  // 1) Garante que o nome está vazio
  cy.get('input[name="nome"]')
    .clear()
    .should('have.value', '');

  // 2) Preenche os demais campos em ISO/HTML5
  cy.get('input[name="data_inicial"]')
    .clear()
    .type('2025-04-09')
    .blur();
  cy.get('input[name="hora"]')
    .clear()
    .type('17:00');
  cy.get('input[name="local"]')
    .clear()
    .type('Quadra C');
  cy.get('input[name="limite_participantes"]')
    .clear()
    .type('6');

  // 3) Clica em Salvar Pelada
  cy.contains('button', /Salvar Pelada|Salvar/i).click();

  // 4) Checa a validação HTML5 do input “nome”
  cy.get('input[name="nome"]').then($el => {
    expect($el[0].checkValidity()).to.be.false;
    expect($el[0].validationMessage).to.be.oneOf([
        'Preencha este campo.', 
        'Please fill out this field.'
      ]);
  });
});
});