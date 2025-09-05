import logging
from datetime import datetime, timezone
from aiogram import Router, F
from aiogram.types import Message
from vpn_client import get_vpn_key
from bot.db.database import enable_vpn_in_db, extend_expires_at, get_user_by_telegram_id

router = Router()


@router.message(F.text == "⚡️ Подключиться")
async def connect_button(message: Message):
    user_id = message.from_user.id
    try:
        user = await get_user_by_telegram_id(user_id)
        is_user_expired = user.expires_at and user.expires_at <= datetime.now(
            timezone.utc
        )
        if is_user_expired:
            await message.answer(
                "Доступ к VPN приостановлен. Для включения требуется оплата."
            )
            return
        vpn_key = await get_vpn_key(
            user_id
        )  # 2) новый либо действующий пользователь (если новый то передам enable: True в create_client)
        if not vpn_key:
            await message.answer("❌ Не удалось получить VPN ключ.")
            return
        if user.expires_at is None:  # новый пользователь
            await enable_vpn_in_db(user_id)  # включение VPN в БД
            await extend_expires_at(
                user_id, days=1
            )  # в БД выставили expires_at (now + trial 1 день)
        text = f"<pre>{vpn_key}</pre>"
        await message.answer(
            f"{text}\n 👆 Это ваш VPN ключ. Коснитесь, чтобы скопировать"
        )
    except Exception as e:
        logging.error(f"Exception in connect_button: {e}")
        await message.answer("❌ Произошла ошибка при подключении.")
