from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from stark.api.routes.admin import router as admin_router
from stark.api.routes.auth import router as auth_router
from stark.api.routes.health import router as health_router
from stark.api.routes.users import router as users_router
from stark.core.config import settings
from stark.core.exception_handlers import register_exception_handlers
from stark.core.logging import configure_logging
from stark.middleware.request_middleware import RequestMiddleware
from stark.middleware.security_headers import SecurityHeadersMiddleware

configure_logging()

app = FastAPI(
    title=settings.app_name,
    summary="Template profissional para APIs REST com FastAPI",
    description="""
API desenvolvida com FastAPI seguindo arquitetura em camadas.

## Recursos

- Autenticação JWT
- Refresh Token com rotação
- Controle de acesso baseado em papéis (RBAC)
- Gerenciamento de usuários
- Gerenciamento de permissões
- Painel administrativo
- Auditoria de ações
- Paginação
- Migrações com Alembic

Esta API utiliza autenticação Bearer Token para os endpoints protegidos.
""",
    version=settings.app_version,
    contact={
        "name": "Stark API",
        "url": "https://github.com/",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.app_env == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )


app.add_middleware(RequestMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

register_exception_handlers(app)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "status": "online",
        "version": settings.app_version,
    }
