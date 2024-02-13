from http import HTTPStatus
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Query
from starlette import status

from wb_data_service.database.deps import DbSession
from wb_data_service.product.models import Product
from wb_data_service.product.repository import ProductRepository
from wb_data_service.product.service import ProductService
from wb_data_service.wb_service.deps import WbServiceSession
from wb_data_shared.exceptions.api_error import WbDataException, WbDataErrorCode
from wb_data_shared.schemas.protocol import WbProductModel, ProductFieldsForGroup, WbProductPriceModel

product_router = APIRouter()


@product_router.post(
    "/",
    response_model=WbProductModel,
    status_code=status.HTTP_200_OK,
    summary="Add product",
    description="Add a product from Wb."
)
async def add_product(nm_id: Annotated[int, Query(description="Product id from Wildberries")],
                      db_session: DbSession,
                      wb_session: WbServiceSession):
    product_repository = ProductRepository(db_session)
    if await product_repository.has_product(nm_id):
        raise WbDataException(
            message="The product has already been added",
            error_code=WbDataErrorCode.PRODUCT_ALREADY_EXIST,
            http_status_code=HTTPStatus.CONFLICT
        )
    service = ProductService(db_session, wb_session)
    service.load_model(nm_id)
    await service.upload_to_db()

    return service.product_db.to_protocol_product()


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


stat_router = APIRouter()


@stat_router.post(
    "/count",
    response_model=list[tuple] | int,
    status_code=status.HTTP_200_OK,
    summary="Get count",
    description="Get the count of product in the base. Specify the fields in the required order for grouping, "
                "if omitted the count of all data in the database."
)
async def stat_count_products(db_session: DbSession,
                              fields: Optional[set[ProductFieldsForGroup]] = None):
    product_repository = ProductRepository(db_session)
    if fields is not None:
        data = await product_repository.get_count_products_grouped(*[getattr(Product, str(item)) for item in fields])
        data = [tuple(item) for item in data]
    else:
        data = await product_repository.get_count_all_products()

    return data


@stat_router.post(
    "/quantity",
    response_model=list[tuple] | int,
    status_code=status.HTTP_200_OK,
    summary="Get quantity",
    description="Get the  of quantity in stock on Wildberries by current database. "
                "Specify the ID of a particular product or specify fields in the desired order for grouping, "
                "if they are omitted - counting all data in the database."
)
async def stat_quantity_products(db_session: DbSession,
                                 nm_id: Annotated[Optional[int], Query(description="Product id from Wildberries")] = None,
                                 fields: Optional[set[ProductFieldsForGroup]] = None):
    product_repository = ProductRepository(db_session)
    if nm_id is not None:
        data = await product_repository.get_quantity_product_by_nm_id(nm_id)
    elif fields is not None:
        data = await product_repository.get_quantity_products_grouped(*[getattr(Product, str(item)) for item in fields])
        data = [tuple(item) for item in data]
    else:
        data = await product_repository.get_quantity_all_products()

    return data


@stat_router.post(
    "/price-history",
    response_model=list[tuple] | list[WbProductPriceModel],
    status_code=status.HTTP_200_OK,
    summary="Get price history",
    description="Get the price history of products from the database. Specify the product id and grouping "
                "fields to get the grouped price history by category for the specified product. Specify only "
                "id to get price history for only one product. Specify only fields to get the price history of "
                "all products grouped by specified fields. Do not specify anything to get the entire price "
                "history of all products."
)
async def stat_product_price_history(db_session: DbSession,
                                     nm_id: Annotated[Optional[int], Query(description="Product id from Wildberries")] = None,
                                     fields: Optional[set[ProductFieldsForGroup]] = None):
    product_repository = ProductRepository(db_session)
    if nm_id is not None and fields is not None:
        prices = await product_repository.get_product_price_grouped_for_product_by_nm_id(
            nm_id,
            *[getattr(Product, str(item)) for item in fields]
        )
        prices = [tuple(item) for item in prices]
    elif fields is not None:
        prices = await product_repository.get_product_prices_grouped(*[getattr(Product, str(item)) for item in fields])
        prices = [tuple(item) for item in prices]
    elif nm_id is not None:
        prices = await product_repository.get_product_prices(nm_id)
        prices = [item.to_protocol_product_price() for item in prices]
    else:
        prices = await product_repository.get_all_product_prices()
        prices = [item.to_protocol_product_price() for item in prices]

    return prices


@stat_router.post(
    "/min-max-price",
    response_model=tuple[int, int],
    status_code=status.HTTP_200_OK,
    summary="Get min and max price",
    description="Get the minimum maximum price for the specified interval in months"
)
async def stat_product_min_max_price_on_monthly_interval(db_session: DbSession,
                                                         nm_id: Annotated[Optional[int], Query(description="Product id from Wildberries")],
                                                         monthly_interval: Annotated[int, Query(ge=1, le=6, description="Count of months")] = 6):
    product_repository = ProductRepository(db_session)
    min_price, max_price = await product_repository.get_min_max_product_price_on_interval(nm_id, monthly_interval)

    return (min_price, max_price)
