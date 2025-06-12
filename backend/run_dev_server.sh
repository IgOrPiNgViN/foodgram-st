#!/bin/bash

if [ -f .env ]; then
  echo "Using .env file"
  set -a
  source .env
fi

if [ -d venv ]; then
  echo "Using venv"
  source venv/bin/activate
  python3 --version
fi

python3 manage.py migrate

if [ ! -d static_backend ]; then
  python3 manage.py collectstatic
  mkdir -p static_backend/media
fi

echo "Launching load_ingredients script"
python3 load_ingredients.py && echo "Ok" || echo "ERROR"

if [[ "${DEMO_DATA}" == "1" ]]; then
  echo "Launching create_test_data script"
  python3 create_test_data.py && echo "Ok" || echo "ERROR"
fi

echo "Running server..."
echo "Debug: $DEBUG"

if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 1 ] ; then
  python3 manage.py runserver "0:8000"
else
  python3 -m gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
