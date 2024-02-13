from re import compile

from wb_data_tg_bot.bot import BaseTelegramBot
from wb_data_tg_bot.config import settings
from wb_data_tg_bot.service_client.client import ServiceClient
from wb_data_tg_bot.service_client.session import ServiceSession
from wb_data_tg_bot.service_client.utils import get_model_in_json_for_telegram_bot, get_base_in_json_for_telegram_bot


class Handlers:

    def __init__(self, bot: BaseTelegramBot, session: ServiceSession):
        self.bot = bot
        self.service_client = ServiceClient(session)

        @bot.message(compile(r"/help"))
        def help_command(text: str):
            return ("*Available commands:*\n"
                    "*nm_id* — Wildberries product id;\n"
                    "*field* — Product fields available for grouping;\n"
                    "*monthly_interval* — Count of months to get statistics on the interval;\n\n"
                    "add \<nmId\>\n"
                    "get \<nmId\>\n"
                    "get all\n"
                    "delete \<nmId\>\n"
                    "stat count \<field1\> \<field2\> \.\.\.\n"
                    "stat count\n"
                    "stat quantity \<nmId\>\n"
                    "stat quantity \<field1\> \<field2\> \.\.\.\n"
                    "stat quantity"
                    "stat price\-history \<nmId\> \<field1\> \<field2\> \.\.\.\n"
                    "stat price\-history \<nmId\>\n"
                    "stat price\-history \<field1\> \<field2\> \.\.\.\n"
                    "stat price\-history\n"
                    "stat min\-max\-price \<nmId\>\n"
                    "stat min\-max\-price \<nmId\> \<monthly\_interval\>\n")

        @bot.message(compile(r"add\s+(\d+)$"))
        def add_product(text: str):
            nm_id = int(text.split(" ")[-1])
            msg = get_model_in_json_for_telegram_bot(self.service_client.add_product(nm_id))
            return msg or "Product not found on Wildberries, if this is not the case, contact support"

        @bot.message(compile(r"get\s+(\d+)$"))
        def get_product(text: str):
            nm_id = int(text.split(" ")[-1])
            msg = get_model_in_json_for_telegram_bot(self.service_client.get_product_by_nm_id(nm_id))
            return msg or f"Product not found, add it: add {nm_id}"

        @bot.message(compile(r"delete\s+(\d+)$"))
        def delete_product(text: str):
            nm_id = int(text.split(" ")[-1])
            msg = self.service_client.delete_product(nm_id)
            return f"The product {nm_id} has been deleted" if msg else "The deleted has failed"

        @bot.message(compile(r"get\s+all$"))
        def get_all_products(text: str):
            msg = get_model_in_json_for_telegram_bot(self.service_client.get_all_products())
            return msg or "Operation has failed"

        @bot.message(compile(r"^stat\s+count\s+.+$"))
        def stat_count_grouped(text: str):
            fields = text.split(" ")[2:]
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_count(*fields))
            return msg or "Get stat count has failed"

        @bot.message(compile(r"stat\s+count$"))
        def stat_count(text: str):
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_count())
            return msg or "Get stat count failed"

        @bot.message(compile(r"stat\s+quantity\s+(\d+)$"))
        def stat_quantity_for_product(text: str):
            nm_id = int(text.split(" ")[-1])
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_quantity(nm_id))
            return msg or "Get stat quantity has failed"

        @bot.message(compile(r"^stat\s+quantity\s+.+$"))
        def stat_quantity_grouped(text: str):
            fields = text.split(" ")[2:]
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_quantity(None, *fields))
            return msg or "Get stat quantity has failed"

        @bot.message(compile(r"stat\s+quantity$"))
        def stat_quantity(text: str):
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_quantity())
            return msg or "Get stat quantity has failed"

        @bot.message(compile(r"stat\s+price-history\s+(\d+)\s+.+$"))
        def stat_price_history_for_product_grouped(text: str):
            nm_id = int(text.split(" ")[2])
            fields = text.split(" ")[3:]
            data = self.service_client.stat_price_history(nm_id, *fields)
            msg = get_base_in_json_for_telegram_bot(data)
            return msg or "Get price history has failed"

        @bot.message(compile(r"stat\s+price-history\s+(\d+)$"))
        def stat_price_history_for_product(text: str):
            nm_id = int(text.split(" ")[-1])
            data = self.service_client.stat_price_history(nm_id=nm_id)
            msg = get_model_in_json_for_telegram_bot(data)
            return msg or "Get price history has failed"

        @bot.message(compile(r"stat\s+price-history\s+.+$"))
        def stat_price_history_grouped(text: str):
            fields = text.split(" ")[2:]
            data = self.service_client.stat_price_history(None, *fields)
            msg = get_base_in_json_for_telegram_bot(data)
            return msg or "Get price history has failed"

        @bot.message(compile(r"stat\s+price-history$"))
        def stat_price_history(text: str):
            data = self.service_client.stat_price_history()
            msg = get_model_in_json_for_telegram_bot(data)
            return msg or "Get price history has failed"

        @bot.message(compile(r"stat\s+min-max-price\s+(\d+)$"))
        def stat_min_max_for_product(text: str):
            nm_id = int(text.split(" ")[-1])
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_min_max_price(nm_id))
            return msg or "Get min max price has failed"

        @bot.message(compile(r"stat\s+min-max-price\s+(\d+)\s+(\d+)$"))
        def stat_min_max_for_product_on_interval(text: str):
            nm_id = int(text.split(" ")[-2])
            interval = int(text.split(" ")[-1])
            msg = get_base_in_json_for_telegram_bot(self.service_client.stat_min_max_price(nm_id, interval))
            return msg or "Get min max price has failed"
