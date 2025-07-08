from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards import one_month_kb, three_months_kb, six_months_kb

router = Router()


@router.callback_query(F.data.in_({"one_month", "three_months", "six_months"}))
async def subscription_handler(callback: CallbackQuery):
    data = callback.data
    if data == "one_month":
        text = "👌 Доступ: 1 месяц"
        kb = one_month_kb()
    elif data == "three_months":
        text = "⚡️ Доступ: 3 месяца"
        kb = three_months_kb()
    else:  # six_months
        text = "🔥 Доступ: 6 месяцев"
        kb = six_months_kb()

    await callback.message.answer(text, reply_markup=kb)
