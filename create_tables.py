import asyncio
from bot.db.user_storage import create_schema, drop_schema

async def main() -> None:
    await drop_schema()
    await create_schema()

if __name__ == "__main__":
    asyncio.run(main())
