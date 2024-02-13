from typing import Optional

from requests import get, post, delete

from wb_data_shared.schemas.protocol import WbProductModel, WbProductPriceModel
from wb_data_tg_bot.config import settings
from wb_data_tg_bot.service_client.session import ServiceSession


class ServiceClient:

    def __init__(self, session: ServiceSession):
        self.session = session
        self.api_url = f"{settings.WB_DATA_SERVICE_HOST_PORT}/api/v1/product"

    def add_product(self, nm_id: int) -> Optional[WbProductModel]:
        resp = post(f"{self.api_url}/?nm_id={nm_id}")
        return None if resp.status_code != 200 else WbProductModel.parse_obj(resp.json())

    def get_product_by_nm_id(self, nm_id: int) -> Optional[WbProductModel]:
        resp = get(f"{self.api_url}/?nm_id={nm_id}")
        return None if resp.status_code != 200 else WbProductModel.parse_obj(resp.json())

    def delete_product(self, nm_id: int) -> bool:
        resp = delete(f"{self.api_url}/?nm_id={nm_id}")
        return resp.status_code == 200

    def get_all_products(self) -> list[WbProductModel]:
        resp = get(f"{self.api_url}/all")
        return None if resp.status_code != 200 else [WbProductModel.parse_obj(item) for item in resp.json()]

    def stat_count(self, *fields) -> Optional[list[tuple] | int]:
        if len(fields) < 1:
            fields = None
        resp = post(f"{self.api_url}/stat/count", json=fields)
        return None if resp.status_code != 200 else resp.json()

    def stat_quantity(self, nm_id: Optional[int] = None, *fields) -> Optional[list[tuple] | int]:
        url = f"{self.api_url}/stat/quantity"
        if nm_id is not None:
            url += f"?nm_id={nm_id}"
        if len(fields) < 1:
            fields = None
        resp = post(url, json=fields)
        return None if resp.status_code != 200 else resp.json()

    def stat_price_history(self, nm_id: Optional[int] = None, *fields):
        url = f"{self.api_url}/stat/price-history"
        if nm_id is not None:
            url += f"?nm_id={nm_id}"
        if len(fields) < 1:
            fields = None
        resp = post(url, json=fields)
        return None if resp.status_code != 200 else resp.json() if fields else [WbProductPriceModel.model_validate(item) for item in resp.json()]

    def stat_min_max_price(self, nm_id: int, monthly_interval: int = 6):
        url = f"{self.api_url}/stat/min-max-price?nm_id={nm_id}&monthly_interval={monthly_interval}"
        resp = post(url)
        return None if resp.status_code != 200 else resp.json()
