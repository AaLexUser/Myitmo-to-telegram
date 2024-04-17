FROM python:3.11-slim as base

RUN mkdir -p /app
WORKDIR /app

RUN useradd --create-home appuser && chown appuser /app

FROM base as poetry-deps

ARG POETRY_VERSION=1.8.2

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

USER appuser
RUN pip install --user pipx
ENV PATH=/home/appuser/.local/bin:$PATH
RUN pipx install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-root --no-cache

