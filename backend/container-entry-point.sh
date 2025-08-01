#!/bin/bash

python3 manage.py migrate

if [ -d static_backend ]; then
  rm -rf static_backend
fi

python3 manage.py collectstatic

cp -r static_backend /static
rm -rf static_backend

if [ ! -d /static/media ]; then
  mkdir -p /static/media
fi

python3 load_ingredients.py && echo "Loading load_ingredients - OK" || echo "Loading load_ingredients - ERROR"

if [[ "${DEMO_DATA}" == "1" ]]; then
  python3 create_test_data.py && echo "Ok" || echo "ERROR"&& echo "Loading create_test_data - OK" || echo "Loading create_test_data - ERROR"
fi


if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 0 ] ; then
 
  python3 manage.py runserver "0:8000"
else

  gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
