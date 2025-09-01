from datetime import datetime, timedelta, timezone

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


def get_trial_expiry_date() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=1)


class User(Base):
    __tablename__ = "users"  # название таблицы в БД (смотри через DBeaver)

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_vpn_enabled: Mapped[bool] = mapped_column(
        default=True,  # по умолчанию True для новых пользователей
        comment="Включен ли VPN для пользователя",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_trial_expiry_date,
        comment="Дата истечения подписки (с учетом free trial на 1 день)",
    )
    first_notified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        comment="Уведомление за 3 дня до истечения срока оплаты",
    )
    second_notified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        comment="Уведомление за 1 день до истечения срока оплаты",
    )
    birthday: Mapped[Date | None] = mapped_column(Date, comment="Дата рождения")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class TelegramEvent(Base):
    __tablename__ = "telegram_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )
