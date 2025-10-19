import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# === Добавляем путь до корня проекта (les16) ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Теперь можно импортировать sql_app
from sql_app.db import settings
from sql_app.models import Base

# Alembic Config object
config = context.config

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей
target_metadata = Base.metadata

# URL для подключения к БД (берём из .env)
DATABASE_URL = settings.sqlalchemy_url


def run_migrations_offline() -> None:
    """Запуск миграций без подключения к БД (offline mode)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Миграции при активном соединении."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций с подключением к asyncpg."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
