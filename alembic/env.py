from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import Base và metadata từ các model SQLAlchemy của bạn
from app.core.db import database  # Nơi định nghĩa Base
from app.modules.users.models.user_model import User  # Import model User

# Cấu hình Alembic
config = context.config

# Thiết lập logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata sẽ trỏ tới metadata từ model của bạn
target_metadata = database.Base.metadata

def run_migrations_offline() -> None:
    """Thực hiện migration ở chế độ offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Thực hiện migration ở chế độ online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
