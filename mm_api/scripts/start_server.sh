#!/bin/bash

# Start asgi server
echo Starting asgi server.

python manage.py makemigrations

python manage.py migrate

exec daphne -b 0.0.0.0 -p 8000 mm_api.asgi:channel_layer


