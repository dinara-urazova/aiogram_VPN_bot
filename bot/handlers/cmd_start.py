from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import start_kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 Привет!  Это Telegram-бот для подключения к VPN.\n"
        "🎁 Вам доступен бесплатный период - 1 день.\n\n"
        "Для начала работы нажмите в меню кнопку ⚡️Подключиться ↓"
    )
    await message.answer(text, reply_markup=start_kb())
