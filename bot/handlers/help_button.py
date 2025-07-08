from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import help_kb

router = Router()

@router.message(F.text == ("❓ Помощь"))
async def help_button(message: Message):
    text = (
        "Если у вас проблемы с подключением, отправьте статус из бота и скриншот из приложения, которым вы пользуетесь для доступа к VPN в поддержку.\n\n"
        "Ниже представлены инструкции для подключения к сервису ↓"
    )
    await message.answer(text, reply_markup=help_kb())


