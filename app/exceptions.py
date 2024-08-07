from fastapi import HTTPException, status


class BookingException(HTTPException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):

        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):

    status_code = status.HTTP_409_CONFLICT
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class BookingDifferenceDate(BookingException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось забронировать номер: дата заезда больше даты выезда."


class BookingManyDays(BookingException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось забронировать номер: бронь больше 30 дней."
