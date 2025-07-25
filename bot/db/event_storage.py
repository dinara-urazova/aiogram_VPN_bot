from bot.db.db_engine import engine
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import TelegramEvent


async def create_telegram_event(telegram_id: int, payload: dict) -> None:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        new_event = TelegramEvent(
            telegram_id=telegram_id,
            payload=payload,
        )
        async_session.add(new_event)
        await async_session.commit()
