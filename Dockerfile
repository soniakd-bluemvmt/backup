FROM python:3.12-slim

WORKDIR /app


COPY pyproject.toml ./ 
COPY src ./src
COPY docker/entrypoint.sh /app/entrypoint.sh
COPY src/alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY docker/check_db.py ./docker/check_db.py


RUN pip install poetry==2.1.3 \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

#RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh



ENTRYPOINT ["sh", "/app/entrypoint.sh"]

CMD ["poetry", "run", "uvicorn", "src.search_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
