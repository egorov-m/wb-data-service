from requests import Session

from wb_data_service.wb_service.api.requests.base import BaseRequests
from wb_data_service.wb_service.utils.params import get_basket_id


class PriceHistoryRequest(BaseRequests):

    url = "https://basket-01.wbbasket.ru/vol<id>/part<id>/<id>/info/price-history.json"
    method = "GET"

    def __init__(self,
                 session: Session,
                 nm_id: int,
                 **kwargs):
        self._process_url(nm_id)

        super().__init__(session, **kwargs)

    def _process_url(self, nm_id: int):
        self.url = (f"https://basket-{get_basket_id(nm_id)}.wbbasket.ru/"
                    f"vol{nm_id // 100000}/"
                    f"part{nm_id // 1000}/"
                    f"{nm_id}/info/price-history.json")

        return self.url

    def get_price_history(self):
        return self.send()
