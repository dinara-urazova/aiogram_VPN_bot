from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config_reader import env_config

engine = create_async_engine(
    env_config.postgresql_url.get_secret_value(),
    echo=True,
)


async_session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
