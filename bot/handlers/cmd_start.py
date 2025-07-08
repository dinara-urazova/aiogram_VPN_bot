from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards import start_kb

router = Router()


@router.message(CommandStart)
async def cmd_start(message: Message):
    text = "👋 Привет!  Это Telegram-бот для подключения к VPN. Вам доступен бесплатный период - 10 дней. Для начала работы нажмите в меню кнопку ⚡️Подключиться ↓"
    await message.answer(text, reply_markup=start_kb())
