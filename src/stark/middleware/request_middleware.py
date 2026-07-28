import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        response.headers["X-Process-Time"] = f"{elapsed:.6f}"

        return response
