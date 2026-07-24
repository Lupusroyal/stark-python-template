from fastapi import FastAPI

from stark.api.routes.health import router as health_router

app = FastAPI(
    title="Stark API",
    version="0.1.0",
)


app.include_router(health_router)


@app.get("/")
def root():
    return {
        "app": "Stark API",
        "status": "online",
        "version": "0.1.0",
    }
