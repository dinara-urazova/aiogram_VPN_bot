from typing import Sequence
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from bot.config_reader import env_config
from bot.db.models import TelegramEvent, User
from bot.user_dto import UserDTO

engine = create_async_engine(
    env_config.postgresql_url.get_secret_value(),
    echo=True,
)


async def get_all_users() -> Sequence[User]:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        result = await async_session.execute(select(User))
        return result.scalars().all()


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await async_session.execute(statement)
        return result.scalar_one_or_none()


async def add_or_update_user(user_dto: UserDTO) -> None:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        user = await get_user_by_telegram_id(user_dto.telegram_id)
        if user is None:  # id пользователя нет в бд
            user = User(
                telegram_id=user_dto.telegram_id,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                username=user_dto.username,
            )
            async_session.add(user)
        else:
            user.first_name = user_dto.first_name
            user.last_name = user_dto.last_name
            user.username = user_dto.username

        await async_session.commit()


async def create_telegram_event(telegram_id: int, payload: dict) -> None:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        new_event = TelegramEvent(
            telegram_id=telegram_id,
            payload=payload,
        )
        async_session.add(new_event)
        await async_session.commit()


async def get_expired_vpn_users() -> Sequence[User]:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        statement = select(User).where(
            User.expires_at <= datetime.now(), User.is_vpn_enabled
        )
        result = await async_session.execute(statement)
        return result.scalars().all()


async def disable_vpn_in_db(telegram_id: int) -> None:
    async with AsyncSession(bind=engine, autoflush=False) as async_session:
        statement = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_vpn_enabled=False)
        )
        await async_session.execute(statement)
        await async_session.commit()
