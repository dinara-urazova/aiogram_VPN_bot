from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_token: SecretStr
    postgresql_url: SecretStr
    owner_chat_id: SecretStr

    panel_url: str
    panel_username: SecretStr
    panel_password: SecretStr
    inbound_id: int

    model_config = SettingsConfigDict(env_file=".env")


env_config = Settings()
