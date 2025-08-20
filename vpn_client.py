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
            if response.status != 200:
                raise RuntimeError(f"Login failed: bad status {response.status}")
            cookie = response.cookies.get("3x-ui")
            if not cookie:
                raise RuntimeError("Login failed: cookie not set")
            return cookie.value


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


async def _get_inbound(session_cookie: str, inbound_id: int, telegram_id: int) -> dict:
    async with aiohttp.ClientSession(cookies={"3x-ui": session_cookie}) as session:
        async with session.get(
            f"{env_config.panel_url}/panel/api/inbounds/get/{inbound_id}",
            ssl=True,
            timeout=30,
        ) as response:
            json_response = await _verify_and_get_json(response)
            if "obj" not in json_response:
                raise RuntimeError("Bad response: obj key not present in response")
            inbound_data = json_response["obj"]
            settings = json.loads(inbound_data["settings"])
            client = next(
                (
                    client
                    for client in settings["clients"]
                    if client["email"] == str(telegram_id)
                ),
                None,
            )  # поиск до первого совпадения, None по умолчанию - если не найдет
            return client, inbound_data


async def _create_and_get_client(
    session_cookie: str, inbound_id: int, telegram_id: int
) -> dict:
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

    return await _get_inbound(session_cookie, inbound_id, telegram_id)


async def _build_vless_key(inbound_dict: dict, client: dict, telegram_id: int) -> str:
    stream_settings = json.loads(inbound_dict["streamSettings"])
    config = {
        "id": client["id"],
        "add": "3x-rus.olegsklyarov.ru",
        "port": inbound_dict["port"],
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


async def get_client_key(telegram_id: int) -> str:
    inbound_id = 1
    session_cookie = await _login()
    client, inbound_dict = await _get_inbound(session_cookie, inbound_id, telegram_id)
    if client is None:
        client, inbound_dict = await _create_and_get_client(
            session_cookie, inbound_id, telegram_id
        )
        assert client is not None
    return await _build_vless_key(inbound_dict, client, telegram_id)
