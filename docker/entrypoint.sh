#!/bin/sh

# Create the database if it doesn't exist using check_db.py
echo "Checking and creating database if it doesn't exist..."
python .docker/check_db.py || exit 1
echo "Database check complete."

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head || exit 1
echo "Alembic migrations complete."

# Execute the command passed to the Docker container (e.g. uvicorn)
exec "$@"
