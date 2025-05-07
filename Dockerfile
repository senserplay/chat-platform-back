FROM python:3.12-slim AS builder

WORKDIR /app

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
        libgl1 \
        libglib2.0-0 \
        libpq-dev \
        build-essential

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8001"