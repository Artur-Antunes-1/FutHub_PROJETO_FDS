# Bug Tracker
## Histórico de Bugs

### Bug 001 - 2025-04-06
- **Descrição**: Erro de importação 'include' não definido em urls.py
- **Impacto**: Impedia execução de migrações
- **Solução**: Adicionada importação faltante
- **Commit Fix**: 536ec7d
- **Arquivos**: project/urls.py
# # #   B u g   0 0 2   -   
 -   D e s c r i � � o :   E r r o   e m   f o r u m / u r l s . p y   c o m   M a i n x V i e w   i n e x i s t e n t e 
 -   S o l u � � o :   C o r r i g i d o   t e m p o r a r i a m e n t e   r e m o v e n d o   a   r o t a 
 -   A r q u i v o s :   p r o j e c t / u r l s . p y ,   f o r u m / v i e w s . p y  
 ### Bug 002 - 2025-04-06
- Descrição: Erro em forum/urls.py com MainxView inexistente
- Solução: Corrigido temporariamente removendo a rota
- Arquivos: project/urls.py, forum/views.py
### Bug 003 - 2025-04-06
- **Descrição**: Estrutura incorreta de pastas (nome 'templates\core' literal)
- **Solução**: Recriada hierarquia correta templates/core/
- **Arquivos**: templates/, BUGS.md
# # #   B u g   0 0 5   -   
 -   D e s c r i � � o :   P � g i n a   r a i z   v a z i a   e   f o r m u l � r i o   m a l   r e n d e r i z a d o 
 -   S o l u � � o :   A d i c i o n a d a   r o t a   r a i z   e   t e m p l a t e   c o r r e t o 
 -   A r q u i v o s :   c o r e / u r l s . p y ,   c o r e / v i e w s . p y ,   t e m p l a t e s / c o r e / h o m e . h t m l ,   t e m p l a t e s / c o r e / p e l a d a _ f o r m . h t m l 
  
 ### Bug 005 - 2025-04-06
- Descrição: Página raiz vazia e formulário mal renderizado
- Solução: Adicionada rota raiz e template correto
- Arquivos: core/urls.py, core/views.py, templates/core/home.html, templates/core/pelada_form.html
### Melhoria 001 - 2025-04-06
- Descrição: Correção de templates e estilização
- Alterações:
  - Página inicial reformulada
  - Formulário de pelada estilizado
  - Placeholders corrigidos
- Arquivos: 
  templates/core/home.html
  templates/core/pelada_form.html
  core/forms.py
### Status Final - 2025-04-06
- Verificação concluída com sucesso
- Estrutura confirmada:
  - Campo 'hora' operacional (TimeField)
  - Todos relacionamentos intactos
- Sistema pronto para produção
