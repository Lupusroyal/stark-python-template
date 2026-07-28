from fastapi import Request
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
    exception = exc
    assert isinstance(exception, UserNotFoundException)

    return JSONResponse(
        status_code=exception.status_code,
        content=exception.detail,
    )


def permission_denied_handler(
    request: Request,
    exc: Exception,
):
    exception = exc
    assert isinstance(exception, PermissionDeniedException)

    return JSONResponse(
        status_code=exception.status_code,
        content=exception.detail,
    )


def invalid_credentials_handler(
    request: Request,
    exc: Exception,
):
    exception = exc
    assert isinstance(exception, InvalidCredentialsException)

    return JSONResponse(
        status_code=exception.status_code,
        content=exception.detail,
    )


def email_exists_handler(
    request: Request,
    exc: Exception,
):
    exception = exc
    assert isinstance(exception, EmailAlreadyExistsException)

    return JSONResponse(
        status_code=exception.status_code,
        content=exception.detail,
    )
