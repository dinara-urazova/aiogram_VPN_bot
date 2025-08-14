import json
import uuid
from urllib.parse import quote, urlencode
import aiohttp
from bot.config_reader import env_config


class VpnClient:
    def __init__(self):

        self.session = aiohttp.ClientSession(cookies=None)
        self.session_cookie = None

    async def login(self) -> dict:
        try:
            response = await self.session.post(
                url=f"{env_config.panel_url}/login",
                data={
                    "username": env_config.panel_username.get_secret_value(),
                    "password": env_config.panel_password.get_secret_value(),
                },
                ssl=True,
                timeout=30,
            )
            data = await self.verify_response(response)

            if data.get("success", False):
                self.session_cookie = response.cookies.get("3x-ui")
                return data

        except Exception as e:
            raise RuntimeError(f"Failed login: error {e}")

    async def verify_response(self, response):
        content_type = response.headers.get("Content-Type", "")
        if response.status != 404 and content_type.startswith("application/json"):
            response = await response.json()
            return response
        else:
            raise RuntimeError("Failed to verify a response")

    async def get_inbounds(self) -> dict:
        response = await self.session.get(
            f"{env_config.panel_url}/panel/api/inbounds/list",
            ssl=True,
            timeout=30,
        )
        data = await self.verify_response(response)
        if not data.get("success", False):
            raise RuntimeError("❌ Getting the inbound list failed")
        return data

    async def get_inbound(self, inbound_id: int) -> dict:
        response = await self.session.get(
            f"{env_config.panel_url}/panel/api/inbounds/get/{inbound_id}",
            ssl=True,
            timeout=30,
        )
        data = await self.verify_response(response)
        if not data.get("success", False):
            raise RuntimeError("❌ Getting the inbound failed")
        return data["obj"]

    async def find_client(self, inbound_id: int, telegram_id: int) -> str | None:
        try:
            inbounds_data = await self.get_inbounds()
            for inbound in inbounds_data["obj"]:
                if inbound["id"] == inbound_id:
                    settings = json.loads(inbound["settings"])
                    for client in settings["clients"]:
                        if client["email"] == telegram_id:
                            return client["id"]
                    return None
            return None

        except Exception as e:
            raise RuntimeError(f"Failed find_client: error {e}")

    async def create_client(self, inbound_id: int, telegram_id: int) -> str:
        client_uuid = str(uuid.uuid4())
        settings = {
            "clients": [
                {
                    "id": client_uuid,
                    "email": telegram_id,
                    "enable": True,
                    "flow": "xtls-rprx-vision",
                }
            ],
            "decryption": "none",
            "fallbacks": [],
        }

        params = {"id": inbound_id, "settings": json.dumps(settings)}

        await self.session.post(
            url=f"{env_config.panel_url}/panel/api/inbounds/addClient",
            data=params,
            ssl=True,
            timeout=30,
        )
        return client_uuid

    async def build_vless_key(
        self, inbound_list: dict, client_uuid: str, telegram_id: int
    ) -> str:
        obj = inbound_list
        settings = json.loads(
            obj["settings"]
        )  # settings is a json string and loads() to turn it into dict
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
    vpn = VpnClient()
    inbound_id = 1
    try:
        await vpn.login()
        client_uuid = await vpn.find_client(inbound_id, telegram_id)
        if client_uuid is None:
            client_uuid = await vpn.create_client(inbound_id, telegram_id)
        inbound_dict = await vpn.get_inbound(inbound_id)
        key_string = await vpn.build_vless_key(inbound_dict, client_uuid, telegram_id)
    except Exception as e:
        return f"Error getting the client key = {e}"
    finally:
        await vpn.session.close()
    return key_string
