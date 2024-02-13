from json import loads
from logging import getLogger

from fastapi import FastAPI, BackgroundTasks
from starlette.requests import Request
from uvicorn import run

from wb_data_tg_bot.bot import BaseTelegramBot
from wb_data_tg_bot.config import settings
from wb_data_tg_bot.handlers import Handlers
from wb_data_tg_bot.service_client.session import ServiceSession
from wb_data_tg_bot.wb_data_logging import setup_logging

logger = getLogger(settings.LOGGER_NAME)


if __name__ == "__main__":
    setup_logging()
    bot: BaseTelegramBot = BaseTelegramBot(token=settings.TELEGRAM_BOT_TOKEN)
    with ServiceSession() as session:
        Handlers(bot, session)
    if settings.TELEGRAM_BOT_MODE == "webhook":
        if settings.TELEGRAM_BOT_WEBHOOK_URL is not None:
            bot.set_webhook(settings.TELEGRAM_BOT_WEBHOOK_URL)

            app = FastAPI(
                title={settings.PROJECT_NAME},
                description=settings.PROJECT_DESCRIPTION,
                version=settings.VERSION,
                docs_url=None,
                redoc_url=None,
                servers=settings.API_SERVERS
            )

            @app.post("/webhook")
            async def telegram_webhook(background_tasks: BackgroundTasks, request: Request):
                data = loads(await request.body())
                if isinstance(data, dict):
                    data = [data]
                background_tasks.add_task(bot.handle_updates, data)
                return {"status": "ok"}

            run(app, host="0.0.0.0", port=settings.SERVER_PORT)
            bot.delete_webhook()
        else:
            logger.error("To use webhook, you need to configure the TELEGRAM_BOT_WEBHOOK_URL parameter")
            exit(-1)
    else:
        bot.run_pulling()
