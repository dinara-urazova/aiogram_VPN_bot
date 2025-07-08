from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import buy_kb

router = Router()


@router.message(F.text == ("🔥 Купить"))
async def buy_button(message: Message):
    text = (
        "Для полного доступа выберите удобный для вас тариф:\n\n"
        "250₽ / 1 мес\n"
        "650₽ / 3 мес\n"
        "1200₽ / 6 мес\n\n"
        "💳 Можно оплатить через:\n"
        "SberPay, СБП, T-Pay, карты и криптовалюты."
    )
    await message.answer(text, reply_markup=buy_kb())
