from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode

from keyboards import (
    start_kb,
    go_back,
    connection_kb,
    buy_kb,
    help_kb,
    one_month_kb,
    three_months_kb,
    six_months_kb,
)

router = Router()


@router.message(CommandStart)
async def cmd_start(message: Message):
    text = "👋 Привет!  Это Telegram-бот для подключения к VPN. Вам доступен бесплатный период - 10 дней. Для начала работы нажмите в меню кнопку ⚡️Подключиться ↓"
    await message.answer(text, reply_markup=start_kb())


@router.message(F.text == "ℹ️ Статус")
async def status_button(message: Message):
    text = (
        "Доступ: ☑️ <b>Пробный период</b>\n"
        "├ Осталось дней: 10\n"
        "└ Активна до: 20.07.2025 18:00"
    )
    await message.answer(text, reply_markup=go_back())


@router.message(F.text == ("⚡️ Подключиться"))
async def connect_button(message: Message):
    text = (
        "Доступ к VPN в 2 шага:\n\n"
        "1️⃣ <b>Скачать</b> – для скачивания приложения\n"
        "2️⃣ <b>Подключить</b> – для добавления подписки\n\n"
        "<b>Настроить VPN вручную:</b>\n"
        '– <a href="https://telegra.ph/Podklyuchenie-v2RayTun-Android-11-09">Инструкция для Android 🤖</a>\n'
        '– <a href="https://telegra.ph/Podklyuchenie-v2raytun-iOS-11-09">Инструкция для iOS/MacOS 🍏</a>\n'
        '– <a href="https://telegra.ph/Nastrojka-VPN-PK-Windows-08-08">Инструкция для Windows 🖥</a>\n\n'
        "<b>Ссылка для ручного подключения</b>\n"
        "<i>Тапните чтобы скопировать в буфер обмена ↓</i>"
    )
    await message.answer(text, reply_markup=connection_kb())


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
    await message.answer(text, reply_markup=connection_kb())


@router.message(F.text == ("❓ Помощь"))
async def help_button(message: Message):
    text = (
        "Если у вас проблемы с подключением, отправьте статус из бота и скриншот из приложения, которым вы пользуетесь для доступа к VPN в поддержку.\n\n"
        "Ниже представлены инструкции для подключения к сервису ↓"
    )
    await message.answer(text, reply_markup=help_kb())


@router.callback_query(F.data == "go_back")
async def go_back_handler(callback: CallbackQuery):
    # удаляем предыдущее сообщение (например, последнее в чате)
    try:
        await callback.message.delete()
        await callback.answer()
    except Exception:
        pass


@router.callback_query(F.data == "one_month")
async def one_month_handler(callback: CallbackQuery):
    text = "👌 Доступ: 1 месяц"
    await callback.message.answer(text, reply_markup=one_month_kb())


@router.callback_query(F.data == "three_months")
async def one_month_handler(callback: CallbackQuery):
    text = "⚡️ Доступ: 3 месяца"
    await callback.message.answer(text, reply_markup=three_months_kb())


@router.callback_query(F.data == "six_months")
async def one_month_handler(callback: CallbackQuery):
    text = "🔥 Доступ: 6 месяцев"
    await callback.message.answer(text, reply_markup=six_months_kb())
