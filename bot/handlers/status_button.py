from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.types import Message

from bot.db import database
from bot.keyboards import go_back_kb

router = Router()


@router.message(F.text == "ℹ️ Статус")
async def status_button(message: Message):
    telegram_id = message.from_user.id
    now = datetime.now(timezone.utc)
    user = await database.get_user_by_telegram_id(telegram_id)
    if not user:
        await message.answer("Пользователь не найден.", reply_markup=go_back_kb())
        return

    status = "✅ Активна" if user.expires_at > now else "❌ Не активна"
    days_left = (user.expires_at - now).days if user.expires_at else 0
    expires_formatted = user.expires_at.strftime("%d.%m.%Y %H:%M %Z")

    text = (
        f"Доступ: {status}\n"
        f"├ Осталось дней: {days_left}\n"
        f"└ Активна до: {expires_formatted}"
    )
    await message.answer(text, reply_markup=go_back_kb())
