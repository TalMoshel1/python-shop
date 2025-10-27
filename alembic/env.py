import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# הוספת תיקיית השורש (shop-api/app) ל-Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

# עכשיו אפשר לייבא דברים מהאפליקציה
from app.core.config import get_settings
from app.db.base import Base
from app.db import models  # חשוב מאוד! כדי ש-Alembic יזהה את כל המודלים

# Alembic Config object
config = context.config

# טעינת הגדרות לוגים
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# הגדרת כתובת ה-DB מתוך environment
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DB_URL)

# מטרה ל-autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
