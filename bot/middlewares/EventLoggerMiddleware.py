from typing import Any, Awaitable, Callable, cast, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from bot.db.event_storage import create_telegram_event


class EventLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = cast(User, data["event_from_user"])
        payload = event.model_dump(exclude_none=True)
        await create_telegram_event(user.id, payload)
        return await handler(event, data)
