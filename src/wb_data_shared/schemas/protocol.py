from datetime import datetime
from typing import Optional

from wb_data_shared.exceptions.api_error import WbDataErrorCode
from wb_data_shared.schemas.base import WbDataBaseModel


class WbDataErrorResponse(WbDataBaseModel):
    error_code: WbDataErrorCode
    message: str


class WbCreateProductModel(WbDataBaseModel):
    nm_id: int
    name: str
    brand: str
    brand_id: int
    site_brand_id: int
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: float
    feedbacks: int
    colors: Optional[str] = None
    quantity: int


class WbUpdateProductModel(WbDataBaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    brand_id: Optional[int] = None
    site_brand_id: Optional[int] = None
    supplier_id: Optional[int] = None
    sale: Optional[int] = None
    price: Optional[int] = None
    sale_price: Optional[int] = None
    rating: Optional[float] = None
    feedbacks: Optional[int] = None
    colors: Optional[str] = None
    quantity: Optional[int] = None


class WbProductModel(WbCreateProductModel):

    created_at: datetime
    updated_at: datetime


class WbProductPriceModel(WbDataBaseModel):
    nm_id: int
    dt: datetime
    price: int
