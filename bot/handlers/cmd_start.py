from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import user_storage
from bot.keyboards import start_kb
from bot.user_dto import UserDTO

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    if not user:
        return

    if not await user_storage.user_exists(user.id):
        user_dto = UserDTO(
            telegram_id=user.id,
            first_name=user.first_name or "Пользователь",
            last_name=user.last_name,
            username=user.username,
        )
        await user_storage.add_user(user_dto)

    print(f"User {message.from_user.id} action detected")



    text = "👋 Привет!  Это Telegram-бот для подключения к VPN. Вам доступен бесплатный период - 10 дней. Для начала работы нажмите в меню кнопку ⚡️Подключиться ↓"
    await message.answer(text, reply_markup=start_kb())
