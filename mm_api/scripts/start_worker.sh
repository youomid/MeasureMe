#!/bin/bash

# Start workers
echo Starting workers.

python manage.py makemigrations

python manage.py migrate

exec python manage.py runworker


