import json
import uuid
from urllib.parse import quote, urlencode

import aiohttp
from aiohttp import ClientResponse

from bot.config_reader import env_config


async def _login() -> str:
    async with aiohttp.ClientSession() as session:
        url = f"{env_config.panel_url}/login"
        data = {
            "username": env_config.panel_username.get_secret_value(),
            "password": env_config.panel_password.get_secret_value(),
        }
        async with session.post(url=url, data=data, ssl=True, timeout=30) as response:
            await _verify_and_get_json(response)
            return response.cookies.get("3x-ui")


async def _verify_and_get_json(response: ClientResponse) -> dict:
    content_type = response.headers.get("Content-Type", "")
    if response.status > 299 or not content_type.startswith("application/json"):
        raise RuntimeError("Bad Response: Failed to verify a response")

    json_response = await response.json()

    if "success" not in json_response:
        raise RuntimeError("Bad response: success key not present in response")

    if json_response["success"] is False:
        raise RuntimeError("Bad response: success is False")

    return json_response


async def _get_inbound(session_cookie: str, inbound_id: int) -> dict:
    async with aiohttp.ClientSession(cookies={"3x-ui": session_cookie}) as session:
        async with session.get(f"{env_config.panel_url}/panel/api/inbounds/get/{inbound_id}", ssl=True,
                               timeout=30) as response:
            json_response = await _verify_and_get_json(response)
            if "obj" not in json_response:
                raise RuntimeError("Bad response: obj key not present in response")
            return json_response["obj"]


async def _find_client(session_cookie: str, inbound_id: int, telegram_id: int) -> dict | None:
    inbound_data = await _get_inbound(session_cookie, inbound_id)
    settings = json.loads(inbound_data["settings"])
    for client in settings["clients"]:
        if client["email"] == telegram_id:  # возможно сравнение строки с int❗️
            return client
    return None


async def _create_and_get_client(session_cookie: str, inbound_id: int, telegram_id: int) -> dict:
    client_uuid = str(uuid.uuid4())
    settings = {
        "clients": [
            {
                "id": client_uuid,
                "email": str(telegram_id),
                "enable": True,
                "flow": "xtls-rprx-vision",
            }
        ],
        "decryption": "none",
        "fallbacks": [],
    }

    params = {"id": inbound_id, "settings": json.dumps(settings)}

    async with aiohttp.ClientSession(cookies={"3x-ui": session_cookie}) as session:
        async with session.post(
                url=f"{env_config.panel_url}/panel/api/inbounds/addClient",
                data=params,
                ssl=True,
                timeout=30,
        ) as response:
            if response.status != 200:
                raise RuntimeError("Failed to add client")

    return await _find_client(session_cookie, inbound_id, telegram_id)


async def _build_vless_key(inbound_list: dict, client: dict, telegram_id: int) -> str:
    obj = inbound_list
    stream_settings = json.loads(obj["streamSettings"])
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
    session_cookie = await _login()
    client = await _find_client(session_cookie, inbound_id, telegram_id)
    if client is None:
        client = await _create_and_get_client(session_cookie, inbound_id, telegram_id)
        assert client is not None
    inbound_dict = await _get_inbound(session_cookie, inbound_id)
    return await _build_vless_key(inbound_dict, client, telegram_id)
