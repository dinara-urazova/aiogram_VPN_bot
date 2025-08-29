import asyncio
from aiogram import Bot
from zoneinfo import ZoneInfo


from bot.db.database import (
    get_users_for_first_notification,
    get_users_for_second_notification,
    mark_first_notified,
    mark_second_notified,
)
from bot.config_reader import env_config


async def send_expiry_reminders(bot: Bot):
    users_first = await get_users_for_first_notification()
    for user in users_first:
        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=(
                    f"Здравствуйте, {user.first_name}!\n\n"
                    "Напоминаем об оплате подписки на VPN.\n"
                    "Чтобы продлить её, нажмите в меню на кнопку '🔥 Купить'."
                ),
            )
            await mark_first_notified(user.telegram_id)
        except Exception as e:
            print(f"Ошибка первого уведомления {user.telegram_id}: {e}")

    users_second = await get_users_for_second_notification()
    for user in users_second:
        expires_msk = user.expires_at.astimezone(ZoneInfo("Europe/Moscow"))
        time_str = expires_msk.strftime("%H:%M %Z")
        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=(
                    f"Здравствуйте, {user.first_name}!\n\n"
                    f"Доступ к VPN будет приостановлен завтра в {time_str}.\n"
                    "Чтобы продлить его, нажмите в меню на кнопку '🔥 Купить'."
                ),
            )
            await mark_second_notified(user.telegram_id)
        except Exception as e:
            print(f"Ошибка второго уведомления {user.telegram_id}: {e}")


async def main() -> None:
    tg_token = env_config.telegram_token.get_secret_value()
    bot = Bot(token=tg_token)
    try:
        await send_expiry_reminders(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
