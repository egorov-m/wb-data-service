from requests import Response

from wb_data_service.wb_service.exceptions import *


EXCEPTION_MAP = {
    400: WbBadRequestError,
    403: WbForbiddenRequestError,
    429: RetriableWbError
}


def get_exception(response: Response) -> WbError:
    err = EXCEPTION_MAP.get(response.status_code, None)

    if err is None:
        return UnknownWbError("Unknown Wb error")

    try:
        return err(msg=response.content.decode(encoding="utf-8"), response=response)
    except UnicodeDecodeError:
        return err(msg="<binary data>", response=response)
