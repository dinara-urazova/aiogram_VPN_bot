from datetime import datetime, timezone
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config_reader import env_config
from bot.db.base import Base
from bot.db.models import User
from bot.user_dto import UserDTO

DATABASE_URL = f"postgresql+asyncpg://{env_config.postgresql_username}:{env_config.postgresql_password.get_secret_value()}@{env_config.postgresql_hostname}:{env_config.postgresql_port}/{env_config.postgresql_database}"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

async def get_all_users() -> List[User]:
    async with async_session as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def user_exists(telegram_id: int) -> bool:
    async with async_session as session:
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await async_session.execute(statement)
        return result.scalar_one_or_none() is not None


async def add_user(user: User) -> None:
    async with async_session as session:
        session.add(user)
        await async_session.commit()


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

