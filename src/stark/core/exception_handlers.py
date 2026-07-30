from typing import cast

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from stark.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    PermissionDeniedException,
    UserNotFoundException,
)


def user_not_found_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(UserNotFoundException, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def permission_denied_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(PermissionDeniedException, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def invalid_credentials_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(InvalidCredentialsException, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def email_exists_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(EmailAlreadyExistsException, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def validation_error_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(RequestValidationError, exc)

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Dados inválidos",
            "details": exc.errors(),
        },
    )


def http_exception_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(HTTPException, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP_ERROR",
            "message": exc.detail,
        },
    )


def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Erro interno do servidor",
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        UserNotFoundException,
        user_not_found_handler,
    )

    app.add_exception_handler(
        PermissionDeniedException,
        permission_denied_handler,
    )

    app.add_exception_handler(
        InvalidCredentialsException,
        invalid_credentials_handler,
    )

    app.add_exception_handler(
        EmailAlreadyExistsException,
        email_exists_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_error_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )
