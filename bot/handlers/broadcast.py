from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.config_reader import env_config
from bot.db import database

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

    users = await database.get_all_users()

    total_users = len(users)
    sent_msg_count = 0
    broadcast_log = []
    for user in users:
        custom_text = f"Здравствуйте, {user.first_name}!\n\n{broadcast_text}"
        try:
            await bot.send_message(chat_id=user.id, text=custom_text)
            sent_msg_count += 1
        except Exception as e:
            broadcast_log.append(f"Ошибка при отправке пользователю {user.id}: {e}")
    await state.clear()
    await message.answer(
        f"Рассылка отправлена! Сообщений отправлено: {sent_msg_count} из {total_users}."
    )
    if broadcast_log:
        text = "<b>Список ошибок:</b>\n"
        for index, error in enumerate(broadcast_log, start=1):
            text += f"{index}. {error}\n"
        await message.answer(text)
