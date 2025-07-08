from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import go_back_kb

router = Router()

@router.message(F.text == "ℹ️ Статус")
async def status_button(message: Message):
    text = (
        "Доступ: ☑️ <b>Пробный период</b>\n"
        "├ Осталось дней: 10\n"
        "└ Активна до: 20.07.2025 18:00"
    )
    await message.answer(text, reply_markup=go_back_kb())