from abc import ABC
from typing import Optional


class BaseResponseException(Exception, ABC):
    def __init__(self, status_code: int, message: Optional[str] = None):
        self.status_code = status_code
        self.message = message


class BadRequestException(BaseResponseException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(400, message or "Bad Request")


class UnauthorizedException(BaseResponseException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(401, message or "Unauthorized")


class ForbiddenException(BaseResponseException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(403, message or "Forbidden")


class NotFoundException(BaseResponseException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(404, message or "Not Found")


class InternalServerErrorException(BaseResponseException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(500, message or "Internal Server Error")
