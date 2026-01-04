from __future__ import annotations

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.models.base import Base

# Import all models so metadata is registered
from app.models.org import Org  # noqa: F401
from app.models.crm import Customer, CustomerIdentity  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.inventory import Inventory  # noqa: F401
from app.models.excel import InventoryFileSource, ExcelInventoryFile, ExcelInventoryRow  # noqa: F401
from app.models.platform import PlatformAccount  # noqa: F401
from app.models.orders import Order, OrderItem  # noqa: F401
from app.models.reservations import OrderItemReservation  # noqa: F401
from app.models.sync import SyncRun  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(url=settings.DATABASE_URL, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section) or {}, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
