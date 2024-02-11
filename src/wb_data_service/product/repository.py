from datetime import timedelta
from http import HTTPStatus
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.sql.functions import count, sum, min, max

from wb_data_service.database.repository import BaseRepository
from wb_data_service.database.utils import (
    NotFoundResultMode,
    menage_db_not_found_result_method,
    menage_db_commit_method,
    CommitMode
)
from wb_data_service.product.models import Product, ProductPrice
from wb_data_shared.exceptions.api_error import WbDataException, WbDataErrorCode
from wb_data_shared.schemas.protocol import WbCreateProductModel, WbProductPriceModel, WbUpdateProductModel
from wb_data_shared.utils import utcnow


class ProductRepository(BaseRepository):
    _product_not_found_exception = WbDataException(
        message="Product not found",
        error_code=WbDataErrorCode.PRODUCT_NOT_FOUND,
        http_status_code=HTTPStatus.NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_product_not_found_exception)
    async def get_product_by_nm_id(self, nm_id: int) -> Product:
        res = await self.session.get(Product, nm_id)
        return res

    async def get_all_products(self) -> Sequence[Product]:
        query = select(Product)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_count_all_products(self) -> int:
        query = select(count(Product.nm_id))
        res = await self.session.execute(query)

        return res.scalar()

    async def get_quantity_all_products(self) -> int:
        query = select(sum(Product.quantity))
        res = await self.session.execute(query)

        return res.scalar()

    async def get_count_products_grouped(self, group_field) -> Sequence:
        query = select(group_field, count(Product.nm_id)).group_by(group_field)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_quantity_products_grouped(self, group_field) -> Sequence:
        query = select(group_field, sum(Product.quantity)).group_by(group_field)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_product_prices(self, nm_id: int) -> Sequence[ProductPrice]:
        query = select(ProductPrice).where(ProductPrice.nm_id == nm_id).order_by(ProductPrice.dt)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_product_prices_grouped(self, group_field) -> Sequence:
        query = (select(group_field, ProductPrice).join(Product, ProductPrice.nm_id == Product.nm_id)
                 .order_by(ProductPrice.dt).group_by(group_field))
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_min_max_product_price_on_interval(self, nm_id: int, monthly_interval: int) -> (int, int):
        months_ago = utcnow() - timedelta(days=monthly_interval * 30)
        query = (select(min(ProductPrice.price), max(ProductPrice.price))
                 .where(ProductPrice.nm_id == nm_id and ProductPrice.dt >= months_ago))
        res = await self.session.execute(query)

        return res.scalars().all()

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_product(self, create_product: WbCreateProductModel) -> Product:
        new_product = Product(
            nm_id=create_product.nm_id,
            name=create_product.name,
            brand=create_product.brand,
            brand_id=create_product.brand_id,
            site_brand_id=create_product.site_brand_id,
            supplier_id=create_product.supplier_id,
            sale=create_product.sale,
            price=create_product.price,
            sale_price=create_product.sale_price,
            rating=create_product.rating,
            feedbacks=create_product.feedbacks,
            colors=create_product.colors,
            quantity=create_product.quantity
        )
        self.session.add(new_product)

        return new_product

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_product(self, nm_id: int, update_product: WbUpdateProductModel) -> Product:
        product: Product = await self.get_product_by_nm_id(nm_id)

        for field, value in update_product.model_dump().items():
            if value is not None:
                setattr(product, field, value)
        self.session.add(product)

        return product

    @menage_db_commit_method(CommitMode.FLUSH)
    async def delete_product(self, nm_id: int):
        product: Product = await self.get_product_by_nm_id(nm_id)
        await self.session.delete(product)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_product_price(self, create_product_price: WbProductPriceModel) -> ProductPrice:
        new_product_price = ProductPrice(
            nm_id=create_product_price.nm_id,
            dt=create_product_price.dt,
            price=create_product_price.price
        )
        self.session.add(new_product_price)

        return new_product_price
