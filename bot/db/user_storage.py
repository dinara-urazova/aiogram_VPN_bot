from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.db_engine import async_session_factory
from bot.db.models import User
from bot.user_dto import UserDTO


async def get_all_users() -> Sequence[User]:
    async with async_session_factory() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def add_or_update_user(user_dto: UserDTO) -> None:

    async def _find_user_by_telegram_id(
        session: AsyncSession, telegram_id: int
    ) -> User | None:
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async with async_session_factory() as session:
        user = await _find_user_by_telegram_id(session, user_dto.telegram_id)
        if user is None:  # id пользователя нет в бд
            user = User(
                telegram_id=user_dto.telegram_id,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                username=user_dto.username,
            )
            session.add(user)
        else:
            user.first_name = user_dto.first_name
            user.last_name = user_dto.last_name
            user.username = user_dto.username

        await session.commit()
