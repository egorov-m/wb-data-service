from signal import signal, SIGINT
from functools import wraps
from inspect import signature
from logging import getLogger
from re import Pattern
from time import sleep
from typing import AnyStr, Callable, Optional

from requests import post, get
from requests.exceptions import RequestException

from wb_data_tg_bot.config import settings


logger = getLogger(settings.LOGGER_NAME)


class BaseTelegramBot:
    """
        Base class for work with Telegram Bot API
    """

    _headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self,
                 token: str,
                 parse_mode: str = "MarkdownV2",
                 disable_web_page_preview: bool = False,
                 disable_notification: bool = False):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self._message_handlers: dict[Pattern[AnyStr], Callable[..., any]] = {}

        logger.debug("Init bot")

    def send_message(self,
                     text,
                     chat_id: int,
                     reply_to_message_id: Optional[int] = None,
                     parse_mode: Optional[str] = None,
                     disable_web_page_preview: Optional[bool] = None,
                     disable_notification: Optional[bool] = None,
                     message_limit: Optional[int] = 4096):
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "parse_mode": parse_mode or self.parse_mode,
            "disable_web_page_preview": disable_web_page_preview or self.disable_web_page_preview,
            "disable_notification": disable_notification or self.disable_notification
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        if len(text) <= message_limit:
            data["text"] = text
            response = post(url, headers=self._headers, json=data)
            logger.info(f"Message sent to [{response.status_code}] {chat_id}")
            return response.json()
        else:
            text_parts = [text[i:i + message_limit] for i in range(0, len(text), message_limit)]
            responses = []
            for part in text_parts:
                data["text"] = part
                response = post(url, headers=self._headers, json=data)
                logger.info(f"Message sent to [{response.status_code}]  {chat_id}")
                responses.append(response.json())

            return responses

    def get_updates(self,
                    offset: Optional[int] = None,
                    limit: Optional[int] = None,
                    timeout: int = 30):
        url = f"{self.api_url}/getUpdates"
        params = {
            "offset": offset,
            "limit": limit,
            "timeout": timeout
        }
        response = get(url, headers=self._headers, params=params)
        logger.debug(f"Get updates")
        return response.json()["result"]

    def set_webhook(self, url: str):
        url = f"{self.api_url}/setWebhook?url={url}"
        response = get(url)
        logger.debug(f"Set webhook [{response.status_code}] {url}")
        return response.json()

    def delete_webhook(self):
        url = f"{self.api_url}/deleteWebhook"
        response = get(url)
        logger.debug(f"Delete webhook [{response.status_code}]")
        return response.json()

    def handle_updates(self, updates: list[dict]):
        if updates:
            for update in updates:
                func = None
                message = update.get("message")
                if message is None:
                    continue
                chat_id = message["chat"]["id"]
                text = update["message"]["text"]
                for regex, f in self._message_handlers.items():
                    match = regex.match(text)
                    if match:
                        func = f
                        break

                if func is not None:
                    kwargs = {
                        "text": text if "text" in signature(func).parameters else None,
                        "chat_id": chat_id if "chat_id" in signature(func).parameters else None,
                        "message": update["message"] if "message" in signature(func).parameters else None,
                    }
                    msg = func(
                        **{k: v for k, v in kwargs.items() if v is not None}
                    )
                else:
                    msg = "The entered command is not correct, try: /help"
                try:
                    self.send_message(str(msg), chat_id)
                except RequestException as e:
                    logger.error(f"Telegram bot API exception: {e}")

    def run_pulling(self):
        offset = None
        signal(SIGINT, self._stop_pulling)
        logger.info("Start pulling")
        while True:
            updates = self.get_updates(offset)
            self.handle_updates(updates)
            if updates:
                offset = updates[-1]["update_id"] + 1
            sleep(settings.TELEGRAM_BOT_PULLING_DELAY_SECONDS)

    @classmethod
    def _stop_pulling(cls, *args, **kwargs):
        logger.info("Stop pulling")
        exit(0)

    def message(self, reg_exp: Pattern[AnyStr]):
        def decorator(f):

            self._message_handlers[reg_exp] = f

            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped

        return decorator
