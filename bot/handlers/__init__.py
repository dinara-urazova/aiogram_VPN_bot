from typing import List
from aiogram import Router
from bot.handlers import (
    broadcast,
    buy_button,
    cmd_start,
    connect_button,
    go_back_handler,
    help_button,
    status_button,
    subscription_handler,
)

def get_routers() -> List[Router]:
    return [
    broadcast.router,
    buy_button.router,
    cmd_start.router,
    connect_button.router,
    go_back_handler.router,
    help_button.router,
    status_button.router,
    subscription_handler.router,

    ]
