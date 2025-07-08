from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.config_reader import env_config
from aiogram.types import Message
from bot.db import user_storage

router = Router()


class BroadcastState(StatesGroup):
    waiting_for_text = State()


@router.message(F.text == "/broadcast")
async def cmd_broadcast(message: Message, state: FSMContext):
    admin_id = int(env_config.owner_chat_id.get_secret_value())
    if message.chat.id != admin_id:
        return
    await state.set_state(BroadcastState.waiting_for_text)
    await message.answer("Введите текст для рассылки:")


@router.message(BroadcastState.waiting_for_text)
async def handle_broadcast_text(message: Message, state: FSMContext, bot: Bot):
    broadcast_text = message.text
    if not broadcast_text:
        await message.answer("❗ Пожалуйста, введите текст для рассылки.")
        return 

    users = await user_storage.get_all_users()

    sent_msg_count = 0
    for user in users:
        try:
            custom_text = f"Здравствуйте, {user.first_name}!\n\n{broadcast_text}"
            sent_msg_count += 1
            await bot.send_message(chat_id=user.telegram_id, text=custom_text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.telegram_id}: {e}")
    await state.clear()
    await message.answer(f"Рассылка отправлена! Сообщений отправлено: {sent_msg_count}.")

