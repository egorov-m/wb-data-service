from contextlib import asynccontextmanager
from http import HTTPStatus
from logging import getLogger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import run

from wb_data_service.api import api_router
from wb_data_service.config import settings
from wb_data_service.database.deps import db_metadata_create_all
from wb_data_service.wb_data_logging import setup_logging
from wb_data_shared.exceptions.api_error import WbDataException, WbDataErrorCode
from wb_data_shared.schemas.protocol import WbDataErrorResponse


logger = getLogger(settings.LOGGER_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    if settings.DB_METADATA_CREATE_ALL:
        await db_metadata_create_all()

    logger.info("Startup server")
    yield
    logger.info("Shutdown server")


api = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=settings.API_SERVERS,
    lifespan=lifespan
)


@api.exception_handler(WbDataException)
async def wb_data_exception_handler(request: Request, exc: WbDataException):
    logger.info(msg=exc)
    return JSONResponse(
        status_code=exc.http_status_code,
        content=WbDataErrorResponse(
            message=exc.message,
            error_code=WbDataErrorCode(exc.error_code)
        ).model_dump()
    )


@api.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(exc, exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "message": "INTERNAL_SERVER_ERROR",
            "error_code": WbDataErrorCode.GENERIC_ERROR
        }
    )


if settings.BACKEND_CORS_ORIGINS:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if settings.DB_METADATA_CREATE_ALL:
    @api.on_event("startup")
    async def startup_event_db_metadata_create_all():
        await db_metadata_create_all()


api.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    run(api, host="0.0.0.0", port=8000, log_level="warning")
