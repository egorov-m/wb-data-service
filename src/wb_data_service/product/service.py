from datetime import datetime
from http import HTTPStatus
from json import loads
from typing import Iterable

from requests import Response

from wb_data_service.database.deps import DbSession
from wb_data_service.product.models import Product, ProductPrice
from wb_data_service.product.repository import ProductRepository
from wb_data_service.wb_service.api.requests.card_detail import CardDetailsRequest
from wb_data_service.wb_service.api.requests.price_history import PriceHistoryRequest
from wb_data_service.wb_service.deps import WbServiceSession
from wb_data_service.wb_service.exceptions import WbError
from wb_data_shared.exceptions.api_error import WbDataException, WbDataErrorCode
from wb_data_shared.schemas.protocol import WbCreateProductModel, WbProductPriceModel


class ProductService:

    _wb_product_not_found = WbDataException(
        message=f"Wildberries product not found",
        error_code=WbDataErrorCode.WILDBERRIES_PRODUCT_NOT_FOUND,
        http_status_code=HTTPStatus.NOT_FOUND
    )

    _req_detail: CardDetailsRequest
    _req_price_history: PriceHistoryRequest
    _detail_response: Response
    _price_history_response: Response
    create_product_model: WbCreateProductModel
    price_history_model: WbProductPriceModel
    product_db: Product

    def __init__(self, db_session: DbSession, wb_session: WbServiceSession):
        self.db_session = db_session
        self.wb_session = wb_session

    def load_model(self, nm_id: int):
        self._load_data(nm_id)
        assert self._detail_response is not None
        assert self._price_history_response is not None

        self.create_product_model = self._resp_detail_to_product_model(self._detail_response)
        self.price_history_model = self._resp_price_history_to_products_price_model(self._price_history_response, nm_id)

    async def upload_to_db(self):
        assert self.create_product_model is not None
        assert self.price_history_model is not None
        product_repository = ProductRepository(self.db_session)
        self.product_db = await product_repository.create_product(self.create_product_model)
        for item in self.price_history_model:
            await product_repository.create_product_price(item)

    def _load_data(self, nm_id: int):
        self._req_detail = CardDetailsRequest(self.wb_session, nm_id)
        self._req_price_history = PriceHistoryRequest(self.wb_session, nm_id)

        try:
            self._detail_response = self._req_detail.get_detail()
            self._price_history_response = self._req_price_history.get_price_history()
        except WbError as e:
            raise WbDataException(
                message=f"Internal server error: {e.__class__.__name__}.",
                error_code=WbDataErrorCode.UNEXPECTED_INTERACTION_ERROR_WITH_WILDBERRIES,
                http_status_code=HTTPStatus.SERVICE_UNAVAILABLE
            )

    @classmethod
    def _resp_detail_to_product_model(cls, resp: Response) -> WbCreateProductModel:
        resp_dict: dict = loads(resp.content.decode("utf-8"))
        data = resp_dict.get("data")
        products = data.get("products") if data is not None else None
        if products is not None and len(products) > 0:
            product = products[0]
            model_dict = {}
            model_dict.update({
                "nm_id": product.get("id"),
                "name": product.get("name"),
                "brand": product.get("brand"),
                "brand_id": product.get("brandId"),
                "site_brand_id": product.get("siteBrandId"),
                "supplier_id": product.get("supplierId"),
                "sale": product.get("sale"),
                "price": product.get("priceU"),
                "sale_price": product.get("salePriceU"),
                "rating": product.get("rating"),
                "feedbacks": product.get("feedbacks")
            })
            for _, value in model_dict.items():
                if value is None:
                    raise cls._wb_product_not_found

            colors = product.get("colors")
            if colors is not None and len(colors) > 0:
                colors = colors[0].get("name")

            sizes = product.get("sizes")
            quantity = 0
            if sizes is not None and len(sizes) > 0:
                sizes = sizes[0].get("stocks")
                if sizes is not None:
                    for item in sizes:
                        qty = item.get("qty")
                        if qty is not None and isinstance(qty, int):
                            quantity += qty

            model_dict.update({
                "colors": colors,
                "quantity": quantity
            })

            model = WbCreateProductModel(**model_dict)

            return model

        else:
            raise cls._wb_product_not_found

    @classmethod
    def _resp_price_history_to_products_price_model(cls, resp: Response, nm_id: int) -> WbProductPriceModel:
        resp_dict = loads(resp.content.decode("utf-8"))
        res = []
        if isinstance(resp_dict, Iterable):
            for item in resp_dict:
                dt = item.get("dt")
                if dt is not None:
                    dt = datetime.fromtimestamp(dt)
                price = item.get("price")
                if price is not None:
                    price = price.get("RUB")
                res.append(WbProductPriceModel(
                    nm_id=nm_id,
                    dt=dt,
                    price=price
                ))

        return res
