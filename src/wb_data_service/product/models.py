from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from wb_data_service.database.core import Base, TimeStampMixin
from wb_data_shared.schemas.protocol import WbProductModel, WbProductPriceModel


class Product(Base, TimeStampMixin):
    nm_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    brand_id = Column(Integer, nullable=False)
    site_brand_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    sale = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    sale_price = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    feedbacks = Column(Integer, nullable=False)
    colors = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)

    def to_protocol_product(self):
        return WbProductModel(
            nm_id=self.nm_id,
            name=self.name,
            brand=self.brand,
            brand_id=self.brand_id,
            site_brand_id=self.site_brand_id,
            supplier_id=self.supplier_id,
            sale=self.sale,
            price=self.price,
            sale_price=self.sale_price,
            rating=self.rating,
            feedbacks=self.feedbacks,
            colors=self.colors,
            quantity=self.quantity,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class ProductPrice(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nm_id = Column(ForeignKey("product.nm_id"), nullable=False)
    dt = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    def to_protocol_product_price(self):
        return WbProductPriceModel(
            nm_id=self.nm_id,
            dt=self.dt,
            price=self.price
        )
