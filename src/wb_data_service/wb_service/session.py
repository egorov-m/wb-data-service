from requests import Session

from wb_data_service.wb_service.config import DEFAULT_USER_AGENT, DEFAULT_ACCEPT_LANGUAGE


class WbSession(Session):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers.update({
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": DEFAULT_ACCEPT_LANGUAGE,
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://www.wildberries.ru",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        })
