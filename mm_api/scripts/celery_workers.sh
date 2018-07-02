#!/bin/bash

# Start celery workers 
echo Starting celery workers.
exec celery worker -A mm_api --app=core.celeryapp:app


