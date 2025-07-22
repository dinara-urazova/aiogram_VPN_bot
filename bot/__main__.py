import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.middlewares.UpdateUserMiddleware import UpdateUserMiddleware
from bot.middlewares.EventLoggerMiddleware import EventLoggerMiddleware
from bot.handlers import get_routers
from bot.config_reader import env_config


tg_token = env_config.telegram_token.get_secret_value()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_routers(*get_routers())

dp.update.outer_middleware(UpdateUserMiddleware())
dp.update.outer_middleware(EventLoggerMiddleware())


async def main():  # Запуск процесса поллинга новых апд
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
