from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import connection_kb
import vpn_client
import logging

router = Router()


@router.message(F.text == "⚡️ Подключиться")
async def connect_button(message: Message):
    user_id = message.from_user.id
    if vpn_client.xui.session_string:
        # Уже залогинен, можно продолжать работу
        logging.info("Already logged in, using existing session")
        res = "✅ Уже авторизованы на панели."
    else:
        try:
            res = await vpn_client.get_client_key(user_id)
            logging.info(f"Login result: {res}")
            if res == "🔥 Successful login":
                res = "✅ Успешно авторизовались на панели."
            else:
                res = "❌ Не удалось авторизоваться."
                
            res = "✅ Успешно авторизовались на панели."
        except Exception as e:
            logging.error(f"Exception in connect_button: {e}")
            res = "❌ Не удалось авторизоваться."
    await message.answer(res)
