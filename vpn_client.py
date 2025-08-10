import json
import logging
import uuid
from urllib.parse import urlencode, quote
from pyxui_async import XUI
from pyxui_async.errors import BadLogin, NotFound
from bot.config_reader import env_config

xui = XUI(full_address=env_config.panel_url, panel="sanaei", session_string=None)
is_logged_in = False


async def get_client_key(telegram_id):
    global is_logged_in
    try:
        if not is_logged_in: # код выполнится только при False (не залогинен)
            username = env_config.panel_username
            password = env_config.panel_password.get_secret_value()
            response = await xui.login(username, password)
            if response is not True:
                logging.error("❌ Login failed")
                return None
            is_logged_in = True
            logging.info("🔥 Successful login")
        inbound_id = 1
        try:
            client = await xui.get_client(inbound_id, email=telegram_id)
            client_uuid = client["id"]
        except NotFound: # новый клиент
            client_uuid = str(uuid.uuid4())
            add_client_response = await xui.add_client(
                inbound_id=1,
                email=telegram_id,
                uuid=client_uuid,
                enable=True,
                flow="xtls-rprx-vision",
            )
            if not add_client_response.get("success", False):  # дб "success": True
                logging.error(f"❌ Adding client failed")
                return None
        inbound_list = await xui.get_inbound(inbound_id=1)  # функция возвращает словарь
        if not inbound_list.get("success", False):
            logging.error(f"❌ Getting the inbound list failed")
            return None
        key_string = await build_vless_key(inbound_list, client_uuid)
        return key_string

    except BadLogin:
        logging.error("❌ Ошибка авторизации")
        return None
    except Exception as e:
        logging.error(f"⚠️ Ошибка при получении ключа: {e}")
        print(f"Error={e}")
        return None


async def build_vless_key(inbound_list: dict, client_uuid):
    obj = inbound_list["obj"]
    settings = json.loads(
        obj["settings"]
    )  # получаем доступ к settings по ключу и парсим их в словарь, так как settings - строка json
    stream_settings = json.loads(obj["streamSettings"])
    clients = settings["clients"]
    client = next((c for c in clients if c["id"] == client_uuid), None) # next здесь выбирает 1 встретившийся экз 
    if client is None:
        logging.error("Клиент не найден в списке inbound")
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



