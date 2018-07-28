# MeasureMe (In Progress)
MeasureMe is a learning project to build a personal analytics realtime distributed data processing system that can be horizontally scaled using docker swarm while maintaining order of events.

## Architecture

![Alt text](/images/mm_diagram.jpg?raw=true "MeasureMe Diagram")

mm_dashboard - a static file server <br />
mm_api - a django based api to handle http requests socket connections from the dashboard <br />
celery_workers - celery workers responsible for processing events and storing in redis/postgres <br />
subscribe_events - consumes events from the RabbitMQ and distributes events to appropriate celery workers <br />
event_source - an api that receives events from registered mobile applications and publishes to RabbitMQ <br />

## MM_Dashboard
The login page and the dashboard. The dashboard contains 4 sections, the monthly history chart, the daily history table, a realtime events feed, and the simulation panel.

![Alt text](/images/login.png?raw=true "Login")
![Alt text](/images/dashboard.png?raw=true "Dashboard")

## MM_API

## Celery_Workers
## Subscribe_Events
## Event_Source
## RabbitMQ
## Redis
## Postgres

