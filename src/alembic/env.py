import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from src.models import Base  # adjust this path to where your models.Base is


# this is the Alembic Config object
config = context.config

# Load logging config from alembic.ini
fileConfig(config.config_file_name)

# Get the URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/search_api")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    ...

def run_migrations_online():
    ...
