from fastapi import APIRouter
from starlette.responses import JSONResponse

api_router = APIRouter(
    default_response_class=JSONResponse
)
