from aiogram import Router, F
from aiogram.types import Message
from bot.db import user_storage
from bot.user_dto import UserDTO

router = Router()


@router.message()
async def register_user(message: Message):
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
