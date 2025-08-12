import json
import uuid
from urllib.parse import quote, urlencode

from bot.config_reader import env_config

async def _xui_login():
    if xui.session_string is not None:
        return

    await xui.login(
        env_config.panel_username.get_secret_value(),
        env_config.panel_password.get_secret_value(),
    )


async def _xui_find_client(inbound_id: int, telegram_id: int) -> str | None:
    try:
        client = await xui.get_client(inbound_id, email=str(telegram_id))
        return client["id"]
    except NotFound:
        return None


async def _xui_create_client(inbound_id: int, telegram_id: int) -> str:
    client_uuid = str(uuid.uuid4())
    add_client_response = await xui.add_client(
        inbound_id=inbound_id,
        email=str(telegram_id),
        uuid=client_uuid,
        enable=True,
        flow="xtls-rprx-vision",
    )

    if not add_client_response.get("success", False):  # дб "success": True
        raise RuntimeError("❌ Adding client failed")

    return client_uuid


async def _xui_get_inbound(inbound_id: int) -> dict:
    inbound_list = await xui.get_inbound(
        inbound_id=inbound_id
    )  # функция возвращает словарь
    if not inbound_list.get("success", False):
        raise RuntimeError("❌ Getting the inbound list failed")
    return inbound_list["obj"]


async def _build_vless_key(
    inbound_list: dict, client_uuid: str, telegram_id: int
) -> str:
    obj = inbound_list
    settings = json.loads(
        obj["settings"]
    )  # получаем доступ к settings по ключу и парсим их в словарь, так как settings - строка json
    stream_settings = json.loads(obj["streamSettings"])
    clients = settings["clients"]
    client = next(
        (c for c in clients if c["id"] == client_uuid), None
    )  # next здесь выбирает 1 встретившийся экз
    if client is None:
        raise RuntimeError("Клиент не найден в списке inbound")

    config = {
        "id": client["id"],
        "add": "3x-rus.olegsklyarov.ru",
        "port": obj["port"],
    }

    data = {
        "type": stream_settings["network"],
        "security": stream_settings["security"],
        "pbk": stream_settings["realitySettings"]["settings"]["publicKey"],
        "fp": stream_settings["realitySettings"]["settings"]["fingerprint"],
        "sni": stream_settings["realitySettings"]["serverNames"][0],
        "sid": stream_settings["realitySettings"]["shortIds"][0],
        "spx": stream_settings["realitySettings"]["settings"]["spiderX"],
        "flow": client["flow"],
    }

    query_str = urlencode(data)
    ps_encoded = quote(f"🇷🇺 SklyarovVPN ({telegram_id})")
    key_string = f"vless://{config['id']}@{config['add']}:{config['port']}?{query_str}#{ps_encoded}"
    return key_string


async def get_client_key(telegram_id: int):
    inbound_id = 1
    await _xui_login()
    client_uuid = await _xui_find_client(inbound_id, telegram_id)
    if client_uuid is None:
        client_uuid = await _xui_create_client(inbound_id, telegram_id)
    inbound_dict = await _xui_get_inbound(inbound_id)
    key_string = await _build_vless_key(inbound_dict, client_uuid, telegram_id)
    return key_string
