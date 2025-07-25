from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class User(Base):
    __tablename__ = "users"  # название таблицы в БД (смотри через DBeaver)

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class TelegramEvent(Base):
    __tablename__ = "telegram_events"

    event_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
