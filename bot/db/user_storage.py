from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from bot.config_reader import env_config
from bot.db.base import Base
from bot.db.models import User
from bot.user_dto import UserDTO


def async_engine():
    return create_async_engine(env_config.postgresql_url.get_secret_value(), echo=False)


async def get_all_users() -> Sequence[User]:
    async with AsyncSession(autoflush=False, bind=async_engine()) as async_session:
        result = await async_session.execute(select(User))
        return result.scalars().all()


async def user_exists(telegram_id: int) -> bool:
    async with AsyncSession(autoflush=False, bind=async_engine()) as async_session:
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await async_session.execute(statement)
        return result.scalar_one_or_none() is not None


async def add_user(user_dto: UserDTO) -> None:
    async with AsyncSession(autoflush=False, bind=async_engine()) as async_session:
        user = User(
            telegram_id=user_dto.telegram_id,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            username=user_dto.username,
        )
        async_session.add(user)
        await async_session.commit()


async def create_schema() -> None:
    async with async_engine().begin() as async_connection:
        await async_connection.run_sync(Base.metadata.create_all)


async def drop_schema() -> None:
    async with async_engine().begin() as async_connection:
        await async_connection.run_sync(Base.metadata.drop_all)
