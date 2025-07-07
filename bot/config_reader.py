from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    telegram_token: SecretStr
    postgresql_database: str
    postgresql_username: str
    postgresql_password: SecretStr
    postgresql_hostname: str
    postgresql_port: str
    owner_chat_id: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


env_config = Settings()
