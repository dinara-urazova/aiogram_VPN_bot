from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_token: SecretStr
    postgresql_url: SecretStr
    owner_chat_id: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


env_config = Settings()
