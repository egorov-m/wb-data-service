from enum import IntEnum
from http import HTTPStatus


class WbDataErrorCode(IntEnum):
    """
        Error codes for API.

        Ranges:
               0-1000: general errors
    """

    # 0-1000: general errors
    GENERIC_ERROR = 0


class WbDataException(Exception):
    """
        Base class for API exceptions.
    """

    message: str
    error_code: int
    http_status_code: HTTPStatus | int

    def __init__(self,
                 message: str,
                 error_code: WbDataErrorCode,
                 http_status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
                 *args):
        super().__init__(message, error_code, http_status_code, *args)
        self.message = message
        self.error_code = error_code
        self.http_status_code = http_status_code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(message='{self.message}', error_code={self.error_code}, http_status_code={self.http_status_code})"
