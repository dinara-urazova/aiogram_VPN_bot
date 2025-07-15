from typing import Any, Awaitable, Callable, cast, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from bot.user_dto import UserDTO

from bot.db.user_storage import add_or_update_user


class UpdateUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = cast(User, data["event_from_user"])

        user_dto = UserDTO(
            telegram_id=user.id,
            first_name=user.first_name or "Пользователь",
            last_name=user.last_name,
            username=user.username,
        )

        await add_or_update_user(user_dto)

        return await handler(event, data)
