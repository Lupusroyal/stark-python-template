from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "USER_NOT_FOUND",
                "message": "Usuário não encontrado",
            },
        )


class PermissionDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "PERMISSION_DENIED",
                "message": "Permissão insuficiente",
            },
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "INVALID_CREDENTIALS",
                "message": "Credenciais inválidas",
            },
        )


class EmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "EMAIL_ALREADY_EXISTS",
                "message": "Email já cadastrado",
            },
        )
