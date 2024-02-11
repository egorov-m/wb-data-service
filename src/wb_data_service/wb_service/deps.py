from typing import Annotated

from fastapi import Depends
from requests import Session

from wb_data_service.wb_service.session import WbSession


def get_wb_session():
    with WbSession() as session:
        yield session


WbServiceSession = Annotated[Session, Depends(get_wb_session)]
