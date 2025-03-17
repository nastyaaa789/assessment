ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ARG UID=1001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --no-interaction --no-ansi --no-root --without dev

USER appuser

COPY ./assessment_service ./assessment_service

EXPOSE 8000

CMD ["python", "-m", "assessment_service"]