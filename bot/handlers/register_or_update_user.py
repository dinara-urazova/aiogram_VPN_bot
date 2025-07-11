from aiogram import Router
from aiogram.types import Message
from bot.db import user_storage
from bot.user_dto import UserDTO

router = Router()


@router.message()
async def register_or_update_user(message: Message):
    user = message.from_user
    if user is None:  # анонимный или группа (не пользователь)
        return

    user_dto = UserDTO(
        telegram_id=user.id,
        first_name=user.first_name or "Пользователь",
        last_name=user.last_name,
        username=user.username,
    )

    await user_storage.add_or_update_user(user_dto)

    print(f"User {user.id} is registered/updated in the db")
