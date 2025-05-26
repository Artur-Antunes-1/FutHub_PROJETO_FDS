describe('História 4 – Sortear times equilibrados', () => {
  const user = { username: 'demo', password: 'pass123' };
  const peladaId = 'test-pelada-id';

  beforeEach(() => {
    cy.login(user.username, user.password);
    cy.visit(`/peladas/${peladaId}/times/`);
  });

  it('Cenário 1: Sorteio com confirmados', () => {
    cy.get('button#sortear').click();
    cy.get('.time1 .jogador').should('have.length.at.least', 2);
    cy.get('.time2 .jogador').should('have.length.at.least', 2);
  });

  it('Cenário 2: Níveis considerados', () => {
    cy.get('button#sortear').click();
    // soma dos níveis deve ser próxima
    cy.get('.time1 .soma-niveis').then($t1 => {
      const v1 = parseInt($t1.text());
      cy.get('.time2 .soma-niveis').should($t2 => {
        const v2 = parseInt($t2.text());
        expect(Math.abs(v1 - v2)).to.be.lessThan(3);
      });
    });
  });

  it('Cenário 3: Refazer sorteio', () => {
    cy.get('button#sortear').click();
    const snapshot1 = cy.get('.time1').invoke('text');
    cy.get('button#refazer').click();
    cy.get('.time1').invoke('text').should(text2 => {
      expect(text2).not.to.eq(snapshot1);
    });
  });

  it('Cenário 4: Excluir não confirmados', () => {
    cy.get('button#sortear').click();
    cy.get('.time1 .jogador:not(.confirmado)').should('not.exist');
  });

  it('Cenário 5: Menos de 4 confirmados — exibe erro', () => {
    // simula menos de 4 confirmados
    cy.get('button#limpar-confirmados').click();
    cy.get('button#sortear').click();
    cy.get('.errorlist').should('contain', 'Mínimo de 4 jogadores');
  });
});
