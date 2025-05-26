describe('História 1 – Criação de pelada', () => {
  const user = { username: 'demo', password: 'pass123' };

  beforeEach(() => {
    cy.login(user.username, user.password);
  });

  it('Cenário 1: Criação bem-sucedida', () => {
    cy.createPelada({
      nome: 'Pelada OK',
      data: '07/04/2025',
      hora: '20:30',
      local: 'Quadra Legal',
      limite: 10
    });
    cy.contains('Pelada OK').should('exist');
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

  it('Cenário 4: Nome em branco — exibe erro', () => {
    cy.createPelada({
      nome: '',
      data: '09/04/2025',
      hora: '17:00',
      local: 'Quadra C',
      limite: 6
    });
    cy.get('.errorlist').should('contain', 'Este campo é obrigatório');
  });

  it('Cenário 5: Data em formato inválido — exibe erro', () => {
    cy.createPelada({
      nome: 'DataErrada',
      data: '2025-04-07',
      hora: '20:00',
      local: 'Quadra D',
      limite: 4
    });
    cy.get('.errorlist').should('contain', 'Formato de data inválido');
  });

  // extra: horário inválido
  it('Horário em formato inválido — exibe erro', () => {
    cy.createPelada({
      nome: 'HoraErrada',
      data: '10/04/2025',
      hora: '8 pm',
      local: 'Quadra E',
      limite: 4
    });
    cy.get('.errorlist').should('contain', 'Formato de hora inválido');
  });
});
