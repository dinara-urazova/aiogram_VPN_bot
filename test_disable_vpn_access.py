import asyncio
from aiogram import Bot

from bot.db.database import get_expired_vpn_users, disable_vpn_in_db
from vpn_client import disable_client
from bot.config_reader import env_config


async def disable_expired_users(bot: Bot):
    users = await get_expired_vpn_users()
    for user in users:
        try:
            telegram_id = user.telegram_id
            await disable_client(telegram_id)  # отключаем VPN в панели
            await disable_vpn_in_db(telegram_id)  # update в БД
            await bot.send_message(
                chat_id=telegram_id,
                text="Доступ к VPN приостановлен, для включения требуется оплата.",
            )
        except Exception as e:
            print(f"Ошибка при отключении {telegram_id}: {e}")


async def main() -> None:
    tg_token = env_config.telegram_token.get_secret_value()
    bot = Bot(token=tg_token)
    await disable_expired_users(bot)
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
