from bot.db.db_engine import async_session_factory
from bot.db.models import TelegramEvent


async def create_telegram_event(telegram_id: int, payload: dict) -> None:
    async with async_session_factory() as session:
        new_event = TelegramEvent(
            telegram_id=telegram_id,
            payload=payload,
        )
        session.add(new_event)
        await session.commit()
