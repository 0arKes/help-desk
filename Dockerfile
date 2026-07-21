FROM python:3.14-slim

WORKDIR /app

RUN pip install poetry

COPY help_desk_api/pyproject.toml .
COPY help_desk_api/poetry.lock .

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

COPY help_desk_api .

ENV PYTHONPATH=/app/src

CMD sh -c "poetry run alembic upgrade head && poetry run uvicorn help_desk_api.main:app --host 0.0.0.0 --port 8000"