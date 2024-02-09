from wb_data_shared.exceptions.api_error import WbDataErrorCode
from wb_data_shared.schemas.base import WbDataBaseModel


class WbDataErrorResponse(WbDataBaseModel):
    error_code: WbDataErrorCode
    message: str
