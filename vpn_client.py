import json
import logging
import uuid
from urllib.parse import urlencode, quote
from pyxui_async import XUI
from pyxui_async.errors import BadLogin
from bot.config_reader import env_config

xui = XUI(full_address=env_config.panel_url, panel="sanaei", session_string=None)


async def get_client_key(telegram_id):
    try:
        # logging.info("Login started")
        username = env_config.panel_username
        password = env_config.panel_password.get_secret_value()
        response = await xui.login(username, password)
        if response is not True:
            # logging.error("❌ Login failed")
            return None
        # logging.info("🔥 Successful login")
        # logging.info("Добавляем клиента...")
        client_uuid = str(uuid.uuid4())
        add_client_response = await xui.add_client(
            inbound_id=1,
            email=telegram_id,
            uuid=client_uuid,
            enable=True,
            flow="xtls-rprx-vision",
        )
        if not add_client_response.get("success", False):  # дб "success": True
            # logging.error(f"❌ Adding client failed")
            return None
        # logging.info("✅ Adding client succeeded")
        # logging.info("🔑 Getting the key")
        inbound_list = await xui.get_inbound(inbound_id=1)  # функция возвращает словарь
        if not inbound_list.get("success", False):
            # logging.error(f"❌ Getting the inbound list failed")
            return None
        # logging.info("❗️ Got the inbound list")
        key_string = await build_vless_key(inbound_list, client_uuid)
        return key_string

    except BadLogin:
        # logging.error("❌ Ошибка авторизации в XUI.")
        return None
    except Exception as e:
        # logging.error(f"⚠️ Ошибка при получении ключа: {e}")
        print(f"Error={e}")
        return None


async def build_vless_key(inbound_list: dict, client_uuid):
    obj = inbound_list["obj"]
    settings = json.loads(
        obj["settings"]
    )  # получаем доступ к settings по ключу и парсим их в словарь, так как settings - строка json
    logging.info(f"Settings={settings}")
    stream_settings = json.loads(obj["streamSettings"])
    clients = settings["clients"]
    client = None  # можно и одной строкой client = next((c for c in clients if c["id"] == client_uuid), None), next здесь выбирает 1 встретившийся экз (как break), в прот случае - None как в словарном методе get
    for c in clients:
        if c["id"] == client_uuid:
            client = c
            break
    if client is None:
        # logging.error("Клиент не найден в списке inbound")
        return None

    config = {
        "id": client["id"],
        "ps": obj["remark"],  # либо SklyarovBot[client.id]
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
    ps_encoded = quote(config["ps"])
    key_string = f"vless://{config['id']}@{config['add']}:{config['port']}?{query_str}#{ps_encoded}"
    logging.info(f"⚡️ Congrats!. Here's the key={key_string}")
    return key_string
