from enum import IntEnum
from functools import wraps
from http import HTTPStatus
from typing import Optional

from sqlalchemy.exc import DatabaseError

from wb_data_shared.exceptions.api_error import WbDataException, WbDataErrorCode


class CommitMode(IntEnum):
    """
    Commit modes for the managed db methods
    """

    NONE = 0
    FLUSH = 1
    COMMIT = 2
    ROLLBACK = 3


def menage_db_commit_method(auto_commit: CommitMode = CommitMode.FLUSH):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match auto_commit:
                case CommitMode.FLUSH:
                    await self.session.flush()
                case CommitMode.COMMIT:
                    await self.session.commit()
                case CommitMode.ROLLBACK:
                    await self.session.rollback()

            return result

        return wrapped_f

    return decorator


class NotFoundResultMode(IntEnum):
    """
    Modes for resolving an empty query result from the database
    """

    NONE = 0
    EXCEPTION = 1


def manage_db_exception_method(ex: type[DatabaseError], raise_ex: Optional[WbDataException] = None):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            try:
                return await f(self, *args, **kwargs)
            except ex:
                if raise_ex is not None:
                    raise raise_ex
        return wrapped_f
    return decorator


def menage_db_not_found_result_method(
        mode: NotFoundResultMode = NotFoundResultMode.EXCEPTION,
        ex: Optional[WbDataException] = None
):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match mode:
                case NotFoundResultMode.NONE:
                    return result
                case NotFoundResultMode.EXCEPTION:
                    if result is None:
                        if ex is None:
                            raise WbDataException(
                                message="Not found",
                                error_code=WbDataErrorCode.NOT_FOUND,
                                http_status_code=HTTPStatus.NOT_FOUND
                            )
                        else:
                            raise ex
                    else:
                        return result

        return wrapped_f

    return decorator
