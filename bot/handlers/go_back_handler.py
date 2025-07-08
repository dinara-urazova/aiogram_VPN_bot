from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "go_back")
async def go_back_handler(callback: CallbackQuery):
    try:
        await callback.message.delete()
        await callback.answer()
    except Exception:
        pass