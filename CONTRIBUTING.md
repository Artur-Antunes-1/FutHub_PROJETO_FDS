# Contributing to FutHub

Bem-vindo(a) ao FutHub! Agradecemos seu interesse em contribuir com este projeto. Este guia explica como configurar o ambiente de desenvolvimento, executar a aplicação, rodar testes e submeter suas contribuições.

---

## 1. Pré-requisitos

* **Git** (versão 2.28+)
* **Python** 3.12
* **Node.js** v18+ e **npm**
* **Virtualenv** (recomendado)

Opcionalmente, Docker/Docker Compose se preferir conteinerizar o serviço.

---

## 2. Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:

   ```bash
   git clone https://github.com/Artur-Antunes-1/FutHub_PROJETO_FDS.git
   cd futhub
   ```

2. Crie e ative um ambiente virtual Python:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .\.venv\Scripts\activate   # Windows
   ```

3. Instale dependências Python:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Instale dependências JavaScript/Cypress:

   ```bash
   npm ci
   ```

---

## 3. Configurações Iniciais

1. Crie o arquivo de variáveis de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Edite `.env` com suas configurações (DATABASE\_URL, SECRET\_KEY, etc.).

3. Rode migrações e colete estáticos:

   ```bash
   python manage.py migrate --noinput
   python manage.py collectstatic --noinput
   ```

---

## 4. Executando a Aplicação

* Para ambiente de desenvolvimento (auto-reload):

  ```bash
  python manage.py runserver
  ```
* Acesse em `http://localhost:8000/`.

---

## 5. Executando Testes

* **E2E com Cypress:**

  ```bash
  npx cypress open      # interface interativa
  npx cypress run       # headless
  ```

---

## 6. Fluxo de Branches e Pull Requests

1. Crie uma branch a partir de `main`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/minha-nova-funcionalidade
   ```

2. Commit suas mudanças localmente com mensagens claras:

   ```bash
   git add .
   git commit -m "feat: adicionar validação de campo x"
   ```

   * Prefixos recomendados: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:` etc.

3. Faça push para o remoto:

   ```bash
   git push origin feature/minha-nova-funcionalidade
   ```

4. Abra um **Pull Request** descrevendo sua alteração e testes realizados.

---

## 7. Boas Práticas de Código

* Siga o **PEP8** para Python. Use `flake8` para verificar:

  ```bash
  flake8
  ```
* Para JavaScript, use ESLint configurado:

  ```bash
  npm run lint
  ```
* Escreva testes para novas funcionalidades e cenários de borda.

---

## 8. Reportando Issues

* Se encontrar bugs ou quiser sugerir melhorias, abra uma **issue** detalhando:

  * Passos para reproduzir
  * Comportamento atual e esperado
  * Logs ou capturas de tela, se possível

---

## 9. Código de Conduta

Seja respeitoso, colaborativo e profissional.

---

Agradecemos sua colaboração! 🚀
