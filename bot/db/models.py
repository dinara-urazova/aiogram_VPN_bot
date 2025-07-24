from sqlalchemy import BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column
from bot.db.base import Base
from datetime import datetime


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
