from json import dumps

from wb_data_shared.schemas.base import WbDataBaseModel


def get_model_in_json_for_telegram_bot(model: WbDataBaseModel | list[WbDataBaseModel]):
    if model is None:
        return None
    if isinstance(model, list):
        return "```json\n[" + ",\n".join([item.model_dump_json(indent=4) for item in model]) + "]\n```"
    else:
        return "```json\n" + model.model_dump_json(indent=4) + "\n```"


def get_base_in_json_for_telegram_bot(model: int | list[tuple]):
    if model is None:
        return None
    if isinstance(model, list):
        return "```json\n" + dumps(model, indent=4) + "\n```"
    else:
        return "```json\n" + str(model) + "\n```"
