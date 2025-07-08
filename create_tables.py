import asyncio
from bot.db.user_storage import create_schema

if __name__ == "__main__":
    asyncio.run(create_schema())
