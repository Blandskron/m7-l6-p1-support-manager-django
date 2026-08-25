#!/bin/sh
set -eu

# La base SQLite se conserva en el volumen Docker entre reinicios.
mkdir -p /app/data
export SQLITE_PATH="${SQLITE_PATH:-/app/data/db.sqlite3}"

python manage.py migrate --noinput

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py createsuperuser --noinput || true
fi

exec "$@"
