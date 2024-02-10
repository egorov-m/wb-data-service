from typing import Iterable

from requests import Session

from wb_data_service.wb_service.api.requests.base import BaseRequests


class CardDetailsRequest(BaseRequests):

    url = ("https://card.wb.ru/cards/v1/detail?"
           "appType=1&"
           "curr=rub&"
           "dest=-1257786&"
           "spp=30&"
           "nm=")

    method = "GET"

    def __init__(self,
                 session: Session,
                 nm_ids: int | Iterable[int],
                 **kwargs):
        self._process_url(nm_ids)

        super().__init__(session, **kwargs)

    def _process_url(self, nm_ids: int | Iterable[int]):
        if isinstance(nm_ids, int):
            self.url += str(nm_ids)
        elif isinstance(nm_ids, Iterable):
            self.url += ";".join(nm_ids)

    def get_detail(self):
        return self.send()
