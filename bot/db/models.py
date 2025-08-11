from datetime import datetime, timedelta

from sqlalchemy import BigInteger, func, ForeignKey, Date
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


def get_trial_expiry_date() -> datetime:
    return datetime.now() + timedelta(days=1)


class User(Base):
    __tablename__ = "users"  # название таблицы в БД (смотри через DBeaver)

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    expires_at: Mapped[datetime | None] = mapped_column(
        default=get_trial_expiry_date,
        comment="Дата истечения подписки (с учетом free trial на 1 день)",
    )
    birthday: Mapped[datetime | None] = mapped_column(Date, comment="Дата рождения")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class TelegramEvent(Base):
    __tablename__ = "telegram_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
