from fastapi import FastAPI, Request
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
    assert isinstance(exc, UserNotFoundException)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def permission_denied_handler(
    request: Request,
    exc: Exception,
):
    assert isinstance(exc, PermissionDeniedException)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def invalid_credentials_handler(
    request: Request,
    exc: Exception,
):
    assert isinstance(exc, InvalidCredentialsException)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


def email_exists_handler(
    request: Request,
    exc: Exception,
):
    assert isinstance(exc, EmailAlreadyExistsException)

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
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
