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


async def find_user_by_telegram_id(
    session: AsyncSession, telegram_id: int
) -> User | None:
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def add_or_update_user(user_dto: UserDTO) -> None:
    async with AsyncSession(autoflush=False, bind=async_engine()) as async_session:
        user = await find_user_by_telegram_id(async_session, user_dto.telegram_id)
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
        await async_session.refresh(user)


async def create_schema() -> None:
    async with async_engine().begin() as async_connection:
        await async_connection.run_sync(Base.metadata.create_all)


async def drop_schema() -> None:
    async with async_engine().begin() as async_connection:
        await async_connection.run_sync(Base.metadata.drop_all)
