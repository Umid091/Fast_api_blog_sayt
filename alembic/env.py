# alembic/env.py
import asyncio
import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from dotenv import load_dotenv

# modellarni import qilamiz — Alembic tanib olishi uchun
from db import Base
from users.models import User
from blog.models import Post, Category, Comment

load_dotenv()

config = context.config
fileConfig(config.config_file_name)

# Bazamizni ko'rsatamiz
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Modellarimizni ko'rsatamiz
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    # Async engine yaratamiz
    connectable = create_async_engine(os.getenv("DATABASE_URL"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Async migration ishga tushirish
asyncio.run(run_migrations_online())