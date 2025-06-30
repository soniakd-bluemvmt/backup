import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Add 'src' to sys.path so Python can resolve search_api.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

# ✅ Now import Base from the correct module
from search_api.models.resource import Base


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
