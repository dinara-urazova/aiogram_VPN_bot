import asyncio
from bot.db.db_engine import engine
from bot.db.base import Base
from bot.db.models import User, TelegramEvent  # noqa: F401

# we need the line above to create tables in db


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main() -> None:
    # await drop_schema()
    await create_schema()


if __name__ == "__main__":
    asyncio.run(main())