import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config_reader import env_config
from bot.handlers import (
    register_or_update_user,
    broadcast,
    buy_button,
    cmd_start,
    connect_button,
    go_back_handler,
    help_button,
    status_button,
    subscription_handler,
)

tg_token = env_config.telegram_token.get_secret_value()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_routers(
    register_or_update_user.router,
    cmd_start.router,
    connect_button.router,
    status_button.router,
    buy_button.router,
    help_button.router,
    go_back_handler.router,
    subscription_handler.router,
    broadcast.router,
)


async def main():  # Запуск процесса поллинга новых апд
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
