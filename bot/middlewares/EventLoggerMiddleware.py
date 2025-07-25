from typing import Any, Awaitable, Callable, cast, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from aiogram.utils.serialization import deserialize_telegram_object_to_python

from bot.db import database


class EventLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = cast(User, data["event_from_user"])
        payload = deserialize_telegram_object_to_python(event)
        await database.create_telegram_event(user.id, payload)
        return await handler(event, data)
