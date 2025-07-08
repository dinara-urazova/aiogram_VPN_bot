from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import connection_kb

router = Router()


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
