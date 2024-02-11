from fastapi import APIRouter
from starlette.responses import JSONResponse

from wb_data_service.product.router import product_router, stat_router

api_router = APIRouter(
    default_response_class=JSONResponse
)

product_router.include_router(stat_router, prefix="/stat", tags=["ProductStat"])
api_router.include_router(product_router, prefix="/product", tags=["Product"])
