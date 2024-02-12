from logging import basicConfig

from wb_data_service.config import settings


LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(name)s: %(message)s"


def setup_logging():
    log_level = str(settings.LOG_LEVEL).upper()
    basicConfig(level=log_level, format=LOG_FORMAT)
