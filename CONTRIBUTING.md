# Contributing to Stark Python Template

Obrigado por considerar contribuir com o Stark Python Template!

Este projeto tem como objetivo fornecer um template moderno, seguro e bem estruturado para desenvolvimento de APIs REST utilizando FastAPI.

## Como contribuir

1. Faça um fork do repositório.
2. Crie uma branch para sua alteração.

```bash
git checkout -b feature/minha-feature
```

3. Faça suas alterações.
4. Execute todos os testes e ferramentas de qualidade.
5. Faça um commit seguindo as convenções do projeto.
6. Abra um Pull Request.

---

# Configuração do ambiente

Clone o projeto:

```bash
git clone https://github.com/Lupusroyal/stark-python-template.git

cd stark-python-template
```

Instale as dependências:

```bash
uv sync
```

Copie o arquivo de configuração:

```bash
cp .env.example .env
```

Suba a aplicação:

```bash
docker compose up -d
```

---

# Qualidade de código

Antes de abrir um Pull Request execute:

```bash
uv run ruff check .

uv run ruff format

uv run mypy .

uv run pytest
```

Ou utilize o pre-commit:

```bash
uv run pre-commit run --all-files
```

Todos os comandos devem finalizar sem erros.

---

# Convenção de commits

Utilizamos o padrão Conventional Commits.

Exemplos:

```text
feat: add role management

fix: resolve refresh token validation

docs: update README

refactor: simplify authentication service

test: add permission endpoint tests

chore: update dependencies
```

---

# Pull Requests

Ao abrir um Pull Request:

- mantenha o escopo pequeno;
- descreva claramente a alteração;
- inclua testes quando necessário;
- atualize a documentação caso aplicável.

---

# Código

Ao contribuir, procure manter:

- tipagem completa;
- código simples e legível;
- responsabilidades bem separadas;
- cobertura de testes;
- compatibilidade com Ruff e MyPy.

---

Obrigado por contribuir!
