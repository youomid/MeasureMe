# MeasureMe
MeasureMe is a learning project to learn how to build a realtime distributed event processing system that can be scaled indefinitely using docker containers with docker swarm.

This system is applied through a simple personal analytics application that receives events from multiple sources such as mobile apps, voice assistant apps, etc. that measure your productivity in some area (fitness, studying, etc.) and aggregates/processes the events to create new insights to your productivity.

## Architecture

![Alt text](/images/mm_diagram.jpg?raw=true "MeasureMe Diagram")

## MM_Dashboard
The login page and the dashboard. The dashboard contains 4 sections, the monthly history chart, the daily history table, a realtime events feed, and the simulation panel.

The files are served using a static file server through an npm script.

`npm run serve-prod`

![Alt text](/images/login.png?raw=true "Login")
![Alt text](/images/dashboard.png?raw=true "Dashboard")

## MM_API
The api is used by the dashboard for all 4 panels as well as the processing pipeline. The api is run using daphne to allow for both http requests and socket connections. 

The api is written using the django framework, and can be run using the commands below.

`daphne -b 0.0.0.0 -p 8000 mm_api.asgi:channel_layer`
`python manage.py runworker`

## Celery_Workers
The celery workers are used to process the events for use by the dashboard. On top of the processing the events is stored in postgres as a django model object, and is also sent to subscribed django channels/groups. In this case, there is only the guest user subscribed to the events group.

The workers will retrieve events from RabbitMQ. These celery workers can be scaled indefinitely by increasing the number of replicas in the docker-compose file. 

`celery worker -A mm_api --app=core.celeryapp:app`

## Subscribe_Events
The subscribe events process is a django command that retrieves events from RabbitMQ and distributes them to different celery workers through RabbitMQ. In this project, we only have 1 celery queue so it just distributes to a single queue.

This process can be scaled indefinitely by increasing the number of replicas in the docker-compose file.

`python manage.py subscribe_events`

## Event_Source
This golang script acts as an api that receives requests to send events to RabbitMQ to be consumed by the subscribe events process. In production, this api would receive events from external applications and should be able to scale very well when receiving millions of events per second.

The script can run using the command below or build the script and run that.

`go build event_source.go`
`go run event_source.go`

## RabbitMQ
RabbitMQ contains 2 queues. The test queue receives events from the event source script and the consumer is the subscribe events process. The celery queue receives events from the subscribe events process and the celery workers consume the events.

## Redis
The redis database is used to store bucket data (processed/aggregated events) for different time periods. For example, the bucket Bucket:guest|1532790000000|1532793599999 represents the data from July 28th, 3:00:00pm to July 28th 3:59:59pm for the user 'guest'. These buckets are used by the monthly history chart and the daily history table.

## Postgres
Postgres is currently being used to store events as a django model object.




