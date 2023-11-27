from fastapi import HTTPException, status


class TicketsException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(TicketsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserIsNotTicketInspectorException(TicketsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Недостаточно прав"


class CannotAddDataToDatabase(TicketsException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class TicketIsNotClosed(TicketsException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "У пользователя имеется не закрытый тикет"
