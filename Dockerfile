FROM python:3.14-slim

RUN apt-get update && apt-get install -yqq \
    make \
    postgresql-17 \
    sudo \
    curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

COPY init.sql /docker-entrypoint-initdb.d/

# postgres config
RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/17/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/17/main/postgresql.conf

# create docker user and db
RUN service postgresql start && \
    su postgres -c "psql --command \"CREATE USER docker WITH SUPERUSER PASSWORD 'docker';\"" && \
    su postgres -c "createdb -O docker docker" && \
    service postgresql stop

COPY run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ./run.sh
