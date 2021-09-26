#!/bin/sh

echo "Waiting for progress..."
if ["$DATABASE"="postgres"]
then
  while !nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "psql started"
fi

python manage.py migrate
exec "$@"