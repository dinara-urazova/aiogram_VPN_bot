import asyncio
from aiogram import Bot, Dispatcher
import logging
from bot.handlers import (
    cmd_start,
    connect_button,
    register_user,
    status_button,
    buy_button,
    help_button,
    go_back_handler,
    subscription_handler,
    broadcast,
)
import sys
from bot.config_reader import env_config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

tg_token = env_config.telegram_token.get_secret_value()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_routers(
    cmd_start.router,
    connect_button.router,
    register_user.router,
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
