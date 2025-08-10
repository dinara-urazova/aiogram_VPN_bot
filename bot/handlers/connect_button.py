import logging
from aiogram import Router, F
from aiogram.types import Message
import vpn_client

router = Router()


@router.message(F.text == "⚡️ Подключиться")
async def connect_button(message: Message):
    user_id = message.from_user.id
    try:
        key = await vpn_client.get_client_key(user_id)
        if key:
            text = f"<pre>{key}</pre>"
            await message.answer(
                f"{text}\n 👆 Это ваш VPN ключ. Коснитесь, чтобы скопировать"
            )
        else:
            await message.answer("❌ Не удалось получить VPN ключ.")
    except Exception as e:
        logging.error(f"Exception in connect_button: {e}")
        await message.answer("❌ Произошла ошибка при подключении.")
