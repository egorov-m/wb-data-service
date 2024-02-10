from time import sleep
from typing import Callable

from requests import Timeout

from wb_data_service.wb_service.config import *
from wb_data_service.wb_service.exceptions import RetriableWbError


def auto_retry(func: Callable, n_retries: int, retry_interval: float):
    n_retries = n_retries or WB_REQUEST_N_RETRIES
    retry_interval = retry_interval or WB_REQUEST_RETRY_INTERVAL

    for i in range(n_retries + 1):
        try:
            return func()
        except (Timeout, RetriableWbError) as e:
            if i == n_retries:
                raise e

        if retry_interval:
            sleep(retry_interval)
