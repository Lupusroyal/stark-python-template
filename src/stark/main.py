from fastapi import FastAPI

from stark.api.routes.auth import router as auth_router
from stark.api.routes.health import router as health_router
from stark.api.routes.users import router as users_router
from stark.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "status": "online",
        "version": settings.app_version,
    }
