#! /bin/bash

wait_for_db()
{
    while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432};
    do sleep 1;
    done;
}

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input )
fi

echo "[INFO] Waiting for DB"
wait_for_db

echo "[INFO] Migrating database"
cd /app
python3 manage.py migrate --noinput

echo "[INFO] Generate Static Files"
python3 manage.py collectstatic --no-input

if [[ $1 == '--watch' ]] ; then
    echo "[INFO] Starting Server in watch mode"
    gunicorn opgincidentresponse.wsgi -b 0.0.0.0:8000 --reload
else
    echo "[INFO] Starting Server"
    gunicorn opgincidentresponse.wsgi -b 0.0.0.0:8000
fi
