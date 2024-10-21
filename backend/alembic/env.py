# alembic/env.py
import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from app.models import Base  # Import your models' Base
from dotenv import load_dotenv

load_dotenv()

# Load the configuration file for logging
fileConfig(context.config.config_file_name)

# Read the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Debugging: Print the DATABASE_URL value to verify
print(f"DATABASE_URL is: {DATABASE_URL}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please set it in your environment variables.")


# Set up metadata for autogeneration
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
