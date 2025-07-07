import asyncio
from aiogram import Bot, Dispatcher

from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import logging
from bot.handlers import cmd_start, status_button, connect_button, buy_button, help_button
import sys
from bot.db.models import User
from bot.user_dto import UserDTO
from bot.db.user_storage import get_all_users, add_user, user_exists
from bot.config_reader import env_config
from aiogram.enums import ParseMode

tg_token = env_config.telegram_token.get_secret_value()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(token=tg_token, parse_mode=ParseMode.HTML)

dp = Dispatcher()
dp.include_routers(cmd_start.router, status_button.router, connect_button)

async def main():  # Запуск процесса поллинга новых апд
    bot = Bot(token=tg_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


# @dp.message(Command("hello"))
# async def cmd_hello(message: Message):
#     await message.answer(
#         f"Hello, <b>{message.from_user.full_name}</b>"
#     )

# @dp.message(F.text)
# async def echo_msg(message: Message):
#     time_now = datetime.now().strftime('%H:%M')
#     await message.answer(
#         f"{message.text}\n\n создано в {time_now}"
#     )




# def process_update_message(message: dict):
#     try:
#         chat_id = message.get("chat", {}).get("id")
#         message_id = message.get("message_id")
#         user = message.get("from")

#         if (
#             not chat_id or not user
#         ):  # убрала `if not message`, чтобы мб принимать 'not msg' от users и добавлять users в db
#             return None

#         telegram_id = user.get("id")
#         first_name = user.get("first_name")
#         last_name = user.get("last_name")
#         username = user.get("username")

#         if not user_storage.user_exists(
#             telegram_id
#         ):  # если нет пользователя в тб БД - добавляем его, если есть - ничего не делаем
#             user = User(telegram_id, first_name, last_name, username)
#             user_storage.add_user(user)


#         elif message_text == "🔥 Купить":
#             delete_message(chat_id, message_id)
#             text, url_buttons = buy_button()
#             send_message(
#                 chat_id=chat_id,
#                 text=text,
#                 parse_mode="HTML",
#                 inline_url_buttons=url_buttons,
#             )

#         elif message_text == "❓ Помощь":
#             delete_message(chat_id, message_id)
#             text, url_buttons = help_button()
#             send_message(
#                 chat_id=chat_id,
#                 text=text,
#                 parse_mode="HTML",
#                 inline_url_buttons=url_buttons,
#             )
#         elif message_text == "/broadcast":
#             global broadcast_mode
#             if chat_id != int(
#                 env_config.owner_chat_id.get_secret_value()
#             ):  # owner_chat_id - SecretStr, chat_id - int
#                 return  # команда от постороннего пользователя (игнорируем)
#             broadcast_mode = True
#             send_message(chat_id=chat_id, text="Введите текст для рассылки: ")

#         elif broadcast_mode and chat_id == int(
#             env_config.owner_chat_id.get_secret_value()
#         ):  # owner_chat_id - SecretStr, chat_id - int
#             broadcast_mode = False  # возвращаем значение по умолчанию
#             text = message_text
#             users = user_storage.get_all_users()
#             print(users)
#             for user in users:
#                 custom_text = f"Здравствуйте, {user.first_name}!\n\n{text}"
#                 send_message(
#                     chat_id=user.telegram_id,
#                     text=custom_text,
#                 )
#             send_message(chat_id=chat_id, text="Рассылка отправлена!")
#             return

#     except Exception as e:
#         print(f"The error is {repr(e)}")


# def process_update_callback(callback_query: dict):
#     try:
#         data = callback_query.get("data")
#         message = callback_query.get("message", {})
#         chat_id = message.get("chat", {}).get("id")
#         message_id = message.get("message_id")

#         if not chat_id or not data:
#             return

#         if data == "go_back":
#             delete_message(chat_id, message_id)
#         else:
#             buy_options = {
#                 "one_month": one_month,
#                 "three_months": three_months,
#                 "six_months": six_months,
#             }
#             if data in buy_options:
#                 text, url_buttons = buy_options[data]()
#                 send_message(chat_id=chat_id, text=text, inline_url_buttons=url_buttons)
#             else:
#                 print(f"Unknown callback data: {data}")

#     except Exception as e:
#         print(f"The error is {repr(e)}")


# next_update_id = 0

# while True:
#     try:  # ask Telegram for new updates
#         response = get_updates(next_update_id)
#         data = response.json()
#         print(data)
#         updates = data["result"]

#         for update in updates:
#             next_update_id = update["update_id"] + 1
#             if "callback_query" in update:
#                 process_update_callback(update["callback_query"])
#             elif "message" in update:
#                 process_update_message(update["message"])
#             else:
#                 continue

#     except Exception as e:
#         print(f"The error is {e}")
#     time.sleep(2)