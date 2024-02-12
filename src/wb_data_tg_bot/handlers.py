from re import compile

from wb_data_tg_bot.bot import BaseTelegramBot


class Handlers:

    def __init__(self, bot: BaseTelegramBot):
        self.bot = bot

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
            return "OK"

        @bot.message(compile(r"get\s+(\d+)$"))
        def get_product(text: str):
            return "**OK**\nqwerty"

        @bot.message(compile(r"get\s+all$"))
        def get_all_products(text: str):
            return "OK"

        @bot.message(compile(r"delete\s+(\d+)$"))
        def delete_product(text: str):
            return "OK"

        @bot.message(compile(r"^stat\s+count\s+.+$"))
        def stat_count_grouped(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+count$"))
        def stat_count(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+quantity\s+(\d+)$"))
        def stat_quantity_for_product(text: str):
            return "OK"

        @bot.message(compile(r"^stat\s+quantity\s+.+$"))
        def stat_quantity_grouped(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+quantity$"))
        def stat_quantity(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+price-history\s+(\d+)\s+.+$"))
        def stat_price_history_for_product_grouped(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+price-history\s+(\d+)$"))
        def stat_price_history_for_product(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+price-history\s+.+$"))
        def stat_price_history_grouped(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+price-history$"))
        def stat_price(test: str):
            return "OK"

        @bot.message(compile(r"stat\s+min-max-price\s+(\d+)$"))
        def stat_min_max_for_product(text: str):
            return "OK"

        @bot.message(compile(r"stat\s+min-max-price\s+(\d+)\s+(\d+)$"))
        def stat_min_max_for_product_on_interval(text: str):
            return "OK"
