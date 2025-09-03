import logging
from aiogram import Router, F
from aiogram.types import Message
from vpn_client import get_client_key, enable_client
from bot.db.database import enable_vpn_in_db, set_expiry_date, get_user_by_telegram_id

router = Router()


@router.message(F.text == "⚡️ Подключиться")
async def connect_button(message: Message):
    user_id = message.from_user.id
    try:
        user = await get_user_by_telegram_id(user_id)
        key = await get_client_key(user_id)
        if key:
            await enable_client(user_id)  # включили VPN в панели
            await enable_vpn_in_db(user_id)  # в БД включили VPN (is_vpn_enabled = True)
            if user.expires_at is None:  # новый пользователь
                await set_expiry_date(
                    user_id, days=1
                )  # в БД выставили expires_at (now + trial 1 день)
            text = f"<pre>{key}</pre>"
            await message.answer(
                f"{text}\n 👆 Это ваш VPN ключ. Коснитесь, чтобы скопировать"
            )
        else:
            await message.answer("❌ Не удалось получить VPN ключ.")
    except Exception as e:
        logging.error(f"Exception in connect_button: {e}")
        await message.answer("❌ Произошла ошибка при подключении.")
