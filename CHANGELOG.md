# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

O formato segue uma organização baseada em versões e categorias de alterações.

---

# [1.0.0] - 2026-08-03

## Added

### API Core
- Estrutura profissional de API REST com FastAPI.
- Arquitetura em camadas:
  - API Routes
  - Services
  - Repositories
  - Models
  - Schemas
  - Core Configuration

### Authentication
- Autenticação JWT.
- Access Token.
- Refresh Token.
- Rotação de Refresh Token.
- Logout com revogação de tokens.
- Hash seguro de senhas.

### Authorization
- Controle de acesso baseado em papéis (RBAC).
- Sistema de permissões.
- Gerenciamento de roles.
- Proteção de endpoints administrativos.

### Audit
- Sistema de auditoria de ações.
- Registro de operações administrativas.
- Auditoria de:
  - usuários;
  - permissões;
  - alterações de papéis;
  - ativações e desativações.

### Security
- Tratamento global de exceções.
- Respostas padronizadas de erro.
- CORS configurável.
- Trusted Host Middleware.
- Security Headers Middleware:
  - X-Content-Type-Options;
  - X-Frame-Options;
  - Referrer-Policy;
  - Content-Security-Policy;
  - Permissions-Policy;
  - Cross-Origin-Opener-Policy;
  - Cross-Origin-Resource-Policy.
- Request ID para rastreamento de requisições.

### Infrastructure
- Dockerfile otimizado.
- Execução do container com usuário não-root.
- Docker Compose com PostgreSQL.
- Healthchecks.
- Configuração via variáveis de ambiente.
- Suporte ao UV para gerenciamento de dependências.

### Quality
- Testes automatizados com Pytest.
- Validação de código com Ruff.
- Formatação automática com Ruff Format.
- Verificação de tipos com MyPy.
- Hooks de pre-commit.
- Pipeline CI com GitHub Actions.

### Documentation
- README profissional.
- Configuração `.env.example`.
- Documentação da API.
- Guia de execução local.

---

## Testing

- 45 testes automatizados passando.
- Cobertura de:
  - autenticação;
  - usuários;
  - permissões;
  - auditoria;
  - erros;
  - headers de segurança;
  - request tracking.

---

## Infrastructure Changes

- PostgreSQL 17 utilizado como banco principal.
- Ambiente de desenvolvimento padronizado via Docker Compose.

---

## Release Notes

Primeira versão estável do Stark Python Template.

Esta versão entrega uma base completa para criação de APIs Python profissionais, com autenticação, autorização, segurança, auditoria, testes automatizados e infraestrutura preparada para evolução em produção.
