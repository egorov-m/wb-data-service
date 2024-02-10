from requests import Session, Response

from wb_data_service.wb_service.config import *
from wb_data_service.wb_service.utils.exception import get_exception
from wb_data_service.wb_service.utils.retry import auto_retry


class BaseRequests:
    """
        Base class for Wb requests.
    """

    url: str
    method: str
    success_codes: set[int] = {200}
    headers: dict[str, str]

    session: Session
    response: Response

    def __init__(self, session: Session, **kwargs):
        kwargs = dict(kwargs)

        timeout = kwargs.pop("timeout", WB_REQUEST_TIMEOUT)
        n_retries = kwargs.pop("n_retries", WB_REQUEST_N_RETRIES)
        retry_interval = kwargs.pop("retry_interval", WB_REQUEST_RETRY_INTERVAL)

        self.session = session
        self.timeout = timeout
        kwargs["timeout"] = timeout
        self.n_retries = n_retries
        self.retry_interval = retry_interval
        self.send_kwargs = kwargs
        self.response = None

    def _attempt(self):
        assert self.url is not None, "send request isn't possible without url"
        assert self.method is not None, "send request isn't possible without http method"

        self.response = self.session.request(self.method, self.url, **self.send_kwargs)
        is_success = self.response.status_code in self.success_codes

        if not is_success:
            raise get_exception(self.response)

    def send(self) -> Response:
        """
            Actually send the request

            :return: `requests.Response` (`self.response`)
        """

        auto_retry(self._attempt, self.n_retries, self.retry_interval)

        assert self.response is not None

        return self.response
