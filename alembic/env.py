import os
import sys
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine # Changed import
from sqlalchemy import pool

from alembic import context

# Add the project root to the Python path so Alembic can find your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DATABASE_URL
from app.database import Base # Import your Base class from database.py
# Import all your models here so that Base.metadata is populated
from app.models import contact_submission 

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


import asyncio

# ... (this goes where the old run_migrations_online function was)

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # set the database URL from your config
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

    connectable = create_async_engine(
            str(DATABASE_URL), # Use the variable directly
            poolclass=pool.NullPool,
        )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

# At the bottom of the file, replace the final if/else block
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Replace the old call with an asyncio run
    asyncio.run(run_migrations_online())

