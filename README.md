# Stark Python Template

Template profissional para APIs REST utilizando Python e FastAPI.

Projeto base desenvolvido com arquitetura em camadas, autenticação, autorização, auditoria, testes automatizados, segurança e ferramentas de qualidade para desenvolvimento e produção.

---

## Recursos

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic para migrations
- JWT Authentication
- Refresh Token com rotação
- Controle de acesso baseado em papéis (RBAC)
- Gerenciamento de usuários
- Gerenciamento de permissões
- Auditoria de ações administrativas
- Paginação
- Tratamento global de exceções
- Validação com Pydantic
- CORS configurável
- Trusted Host em produção
- Security Headers
- Content Security Policy (CSP)
- Request ID para rastreamento
- Logging estruturado
- Docker e Docker Compose
- Pytest
- MyPy
- Ruff
- UV

---

# Stack

- Python 3.12+
- FastAPI
- Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- UV

---

# Estrutura do projeto

```text
.
├── src/
│   └── stark/
│       ├── api/
│       │   └── routes/
│       ├── core/
│       ├── dependencies/
│       ├── middleware/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       └── services/
│
├── tests/
├── alembic/
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

---

# Configuração

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Configure as variáveis necessárias:

```env
APP_NAME=Stark API
APP_VERSION=0.1.0
APP_ENV=development

DEBUG=false

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/stark_db

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Nunca utilize a chave padrão em ambientes reais.

---

# Instalação

Instale as dependências:

```bash
uv sync
```

---

# Executando a aplicação

A aplicação utiliza Docker Compose como ambiente principal.

Subir os serviços:

```bash
make run
```

ou:

```bash
docker compose up -d
```

Serviços iniciados:

- API FastAPI
- PostgreSQL

Verificar containers:

```bash
docker compose ps
```

---

# API

A aplicação estará disponível em:

```
http://localhost:8000
```

Documentação Swagger:

```
http://localhost:8000/docs
```

Documentação ReDoc:

```
http://localhost:8000/redoc
```

Health check:

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "healthy"
}
```

---

# Banco de dados

As migrations são gerenciadas pelo Alembic.

Executar migrations:

```bash
alembic upgrade head
```

ou:

```bash
make migrate
```

Criar uma nova migration:

```bash
alembic revision --autogenerate -m "descricao"
```

---

# Autenticação

A API utiliza autenticação JWT com Bearer Token.

Fluxo:

## Login

Endpoint:

```
POST /auth/login
```

Retorna:

- access_token
- refresh_token

Exemplo de utilização:

```
Authorization: Bearer TOKEN
```

Tokens possuem:

- expiração configurável;
- refresh token com rotação;
- revogação no logout.

---

# Controle de acesso (RBAC)

A autorização é baseada em papéis e permissões.

Exemplo:

```
ADMIN

├── users.read
├── users.update
├── permissions.create
└── audit.read
```

Permissões podem ser associadas aos papéis dos usuários.

---

# Auditoria

Ações administrativas importantes são registradas.

Exemplos:

- criação de permissões;
- alteração de permissões;
- exclusão de permissões;
- alteração de papéis;
- ativação/desativação de usuários.

Cada registro contém:

- usuário responsável;
- ação executada;
- alvo da ação;
- detalhes;
- data e hora.

---

# Segurança

A aplicação possui:

## Headers de segurança

Incluindo:

- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy
- Content-Security-Policy
- Cross-Origin-Opener-Policy
- Cross-Origin-Resource-Policy

## Request Tracking

Cada requisição recebe:

```
X-Request-ID
```

Também é informado:

```
X-Process-Time
```

para acompanhamento do tempo de processamento.

## Trusted Host

O controle de hosts permitidos é ativado em ambiente de produção.

---

# Testes

Executar todos os testes:

```bash
make test
```

ou:

```bash
uv run pytest
```

O projeto possui testes cobrindo:

- autenticação;
- usuários;
- permissões;
- RBAC;
- auditoria;
- tratamento de erros;
- segurança.

---

# Qualidade de código

## Ruff

Lint:

```bash
make lint
```

Formatação:

```bash
make format
```

## MyPy

Verificação de tipos:

```bash
uv run mypy .
```

---

# Desenvolvimento

Comandos disponíveis:

## Instalar dependências

```bash
make install
```

## Executar aplicação

```bash
make run
```

## Executar testes

```bash
make test
```

## Verificar código

```bash
make lint
```

## Formatar código

```bash
make format
```

## Limpar arquivos temporários

```bash
make clean
```

---

# Ambiente de produção

Antes do deploy:

- alterar `SECRET_KEY`;
- configurar variáveis de ambiente;
- utilizar banco PostgreSQL gerenciado;
- definir:

```env
APP_ENV=production
```

- configurar:

```env
ALLOWED_HOSTS
CORS_ORIGINS
```

- revisar logs e monitoramento.

---

# Licença

MIT
