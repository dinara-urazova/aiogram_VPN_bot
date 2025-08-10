from pyxui_async import XUI
from pyxui_async.errors import BadLogin
from bot.config_reader import env_config
import logging
import uuid
import json
from pyxui_async.config_gen import config_generator
from urllib.parse import urlencode, quote

xui = XUI(
    full_address=env_config.panel_url,
    panel="sanaei",
    session_string=None
)

async def get_client_key(telegram_id):
    try:
        logging.info("Login started")
        username = env_config.panel_username
        password = env_config.panel_password.get_secret_value()
        response = await xui.login(username, password)
        if response is True:
            logging.info(f"🔥 Successful login. Response={response}")
            logging.info("Добавление клиента...")
            client_uuid = str(uuid.uuid4())
            add_client_response = await xui.add_client(
                inbound_id=1,  # ID входящего подключения, зависит от твоей панели
                email=telegram_id,  # Можешь формировать динамически
                uuid = client_uuid,
                enable=True,
                flow="xtls-rprx-vision",
            )
            if add_client_response.get("success", False):
                logging.info(f"Adding client succeeded. Response={add_client_response}")
                print("✅ Клиент успешно добавлен")
                logging.info("Getting the key")
                key_response = await xui.get_inbound(inbound_id=1) # возвращает словарь
                logging.info(f"🔥 Success. Response={key_response}")
                obj = key_response["obj"]
                settings = json.loads(obj["settings"]) # получаем доступ к settings по ключу и парсим их в словари, так как settings - строка json
                stream_settings = json.loads(obj["streamSettings"])
                clients = settings["clients"]
                for c in clients:
                    if c["id"] == client_uuid:
                        client = c
                        break
                    else:
                        logging.error("Клиент не найден в списке inbound")
                        client = None

                config = {
                        "id": client["id"],
                        "ps": obj["remark"], # либо SklyarovBot[client.id]
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
                logging.info(f"🔥 Success. Here's the key={key_string}")
                return key_string
            
            else:
                logging.error(f"Adding client failed. Response={add_client_response}")
                return None
        
    except BadLogin:
        logging.error("❌ Ошибка авторизации в XUI.")
        return None
    except Exception as e:
        logging.error(f"⚠️ Ошибка при получении ключа: {e}")
        return None




from urllib.parse import urlencode, quote

def config_generator(protocol: str, config: dict, data: dict) -> str:
    # Параметры, которые пойдут в query string
    params = {k: v for k, v in data.items() if v is not None}

    query = urlencode(params, quote_via=quote)
    
    return f"{protocol}://{config['id']}@{config['add']}:{config['port']}?{query}#{quote(config['ps'])}"


# Данные
config = {
    "ps": "Vless Russia",
    "add": "3x-rus.olegsklyarov.ru",
    "port": "443",
    "id": "d9769c61-fc9d-44fc-bf4f-9b157f68e614"
}

data = {
    "type": "tcp",
    "security": "reality",
    "pbk": "WOJx3obJWCUIxj3hJWdfIhTOm6gFA6wLGRlvD5KjBX0",
    "fp": "firefox",
    "sni": "yahoo.com",
    "sid": "5483",
    "spx": "/",
    "flow": "xtls-rprx-vision"
}

# Генерация
print(config_generator("vless", config, data))