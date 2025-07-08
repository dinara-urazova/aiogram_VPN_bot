from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config_reader import env_config
from aiogram.types import Message
from bot.db import user_storage

router = Router()


class BroadcastState(StatesGroup):
    waiting_for_text = State()


@router.message(F.text == "/broadcast")
async def cmd_broadcast(message: Message, state: FSMContext):
    if message.chat.id != int(env_config.owner_chat_id.get_secret_value()):
        return
    await state.set_state(BroadcastState.waiting_for_text)
    await message.answer("Введите текст для рассылки:")


@router.message(BroadcastState.waiting_for_text)
async def handle_broadcast_text(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    broadcast_text = message.text

    users = await user_storage.get_all_users()

    for user in users:
        try:
            custom_text = f"Здравствуйте, {user.first_name}!\n\n{broadcast_text}"
            await bot.send_message(chat_id=user.telegram_id, text=custom_text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.telegram_id}: {e}")

    await message.answer("Рассылка отправлена!")
