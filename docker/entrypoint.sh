#!/bin/sh

echo "Checking and creating database if it doesn't exist..."
poetry run python docker/check_db.py || exit 1
echo "Database check complete."

echo "Running Alembic migrations..."
poetry run alembic upgrade head || exit 1
echo "Alembic migrations complete."

exec "$@"
