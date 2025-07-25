from sqlalchemy.ext.asyncio import create_async_engine
from bot.config_reader import env_config

engine = create_async_engine(
    env_config.postgresql_url.get_secret_value(),
    echo=True,
)