from typing import Annotated

from fastapi import APIRouter, Query
from starlette import status

from wb_data_service.database.deps import DbSession
from wb_data_service.product.repository import ProductRepository
from wb_data_shared.schemas.protocol import WbProductModel


product_router = APIRouter()


@product_router.get(
    "/",
    response_model=WbProductModel,
    status_code=status.HTTP_200_OK,
    summary="Get product",
    description="Get product from the database by product id."
)
async def get_product_by_nm_id(nm_id: Annotated[int, Query(description="Product id from Wildberries")],
                               db_session: DbSession):
    product_repository = ProductRepository(db_session)
    product = await product_repository.get_product_by_nm_id(nm_id)

    return product.to_protocol_product()


@product_router.get(
    "/all",
    response_model=list[WbProductModel],
    status_code=status.HTTP_200_OK,
    summary="Get all products",
    description="Get all products from the database."
)
async def get_all_products(db_session: DbSession):
    product_repository = ProductRepository(db_session)
    products = await product_repository.get_all_products()

    return [product.to_protocol_product() for product in products]


@product_router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Delete product",
    description="Delete product from the database by product id."
)
async def delete_product_by_nm_id(nm_id: Annotated[int, Query(description="Product id from Wildberries")],
                                  db_session: DbSession):
    product_repository = ProductRepository(db_session)
    await product_repository.delete_product(nm_id)
