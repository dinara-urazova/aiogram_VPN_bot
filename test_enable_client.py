import asyncio

from bot.db.base import Base
from bot.db.database import engine
from bot.db.models import TelegramEvent, User, Payment  # noqa: F401
from vpn_client import set_client_traffic


async def main() -> None:
    # await drop_schema()
    await set_client_traffic(1059125420, True)


if __name__ == "__main__":
    asyncio.run(main())
