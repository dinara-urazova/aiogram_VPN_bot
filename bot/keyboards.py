from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="ℹ️ Статус")
    kb.button(text="⚡️ Подключиться")
    kb.button(text="🔥 Купить")
    kb.button(text="❓ Помощь")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def go_back() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="go_back")
    return kb.as_markup(resize_keyboard=True)


def connection_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Скачать Android 🤖", url="https://play.google.com/store/apps/details?id=com.v2raytun.android&hl=ru&gl=US")
    kb.button(text="Подключить Android 🤖", url="https://apps.artydev.ru/?url=v2raytun://import/https://u.mrzb.artydev.ru/c/2f18b7c0x3f20f8ac#MatadoraVPN")
    kb.button(text="Скачать iOS 🍏", url="https://apps.apple.com/ru/app/v2raytun/id6476628951")
    kb.button(text="Подключить iOS 🍏", url="https://apps.artydev.ru/?url=v2rayTun://import/https://u.mrzb.artydev.ru/c/2f18b7c0x3f20f8ac#MatadoraVPN")
    kb.button(text="Скачать Windows 🖥️", url="Hiddify-Windows-Setup-x64.exe")
    kb.button(text="Подключить Windows 🖥️", url="https://apps.artydev.ru/?url=hiddify://import/https://u.mrzb.artydev.ru/c/2f18b7c0x3f20f8ac")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def buy_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button( text="✅ 1 Месяц", callback_data="one_month")
    kb.button( text="🔥 3 Месяца", callback_data="three_months")
    kb.button( text="🚀 6 Месяцев", callback_data="six_months")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def help_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button( text="Подключить iOS/MacOS 🍏", url="https://telegra.ph/Podklyuchenie-v2raytun-iOS-11-09")
    kb.button( text="Подключить Android 🤖", url="https://telegra.ph/Podklyuchenie-v2RayTun-Android-11-09")
    kb.button( text="Подключить Windows 🖥️", url="https://telegra.ph/Nastrojka-VPN-PK-Windows-08-08")
    kb.button( text="🆘Поддержка", url="https://t.me/olegsklyarov")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def one_month_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button( text="Оплатить!", url="https://yoomoney.ru/checkout/payments/v2/contract?orderId=2fd80e8e-000f-5001-9000-116ba49e2301")
    kb.button( text="Оплатить криптовалютой!", url="https://pay.heleket.com/pay/82849eb2-6993-4f1a-bfef-634363fe0e33")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def three_months_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button( text="Оплатить!", url="https://yoomoney.ru/checkout/payments/v2/contract?orderId=2fd81412-000f-5000-b000-16758ebff8c7")
    kb.button( text="Оплатить криптовалютой!", url="https://pay.heleket.com/pay/e5604090-8520-409f-9f29-f267b0342bc3")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def six_months_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button( text="Оплатить!", url="https://yoomoney.ru/checkout/payments/v2/contract?orderId=2fd80e8e-000f-5001-9000-116ba49e2301")
    kb.button( text="Оплатить криптовалютой!", url="https://pay.heleket.com/pay/82849eb2-6993-4f1a-bfef-634363fe0e33")
    kb.button(text="Назад", callback_data="go_back")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

