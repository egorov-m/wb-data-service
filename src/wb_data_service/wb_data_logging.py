from logging import basicConfig, getLogger
from math import ceil
from typing import Callable

from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from wb_data_service.config import settings
from wb_data_shared.utils import utcnow

LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(name)s: %(message)s"


def setup_logging():
    log_level = str(settings.LOG_LEVEL).upper()
    basicConfig(level=log_level, format=LOG_FORMAT)


logger = getLogger(settings.LOGGER_NAME)


class WbDataRouterLoggerMiddleware:
    async def __call__(
            self,
            request: Request,
            call_next: Callable,
            *args,
            **kwargs
    ):
        start_time = utcnow().timestamp()
        exception_object = None

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            response = Response(
                content=response_body,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            exception_object = ex
        else:
            response_body = b''
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        duration: int = ceil((utcnow().timestamp() - start_time) * 1000)

        message: str = (f"{'Error' if exception_object else 'Response'} "
                        f"{response.status_code} "
                        f"{request.method} "
                        f"\"{str(request.url)}\" "
                        f"{duration} ms")

        logger.info(message, exc_info=exception_object)

        return response
