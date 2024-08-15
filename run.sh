#!/bin/bash

set -e

service postgresql start

until su postgres -c "pg_isready"; do
  echo "Waiting for postgres..."
  sleep 2
done

su postgres -c "psql -d docker -a -f /docker-entrypoint-initdb.d/init.sql"

make prod
