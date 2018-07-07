# MeasureMe (In Progress)
MeasureMe is a learning project to build a personal analytics realtime distributed data processing system that can be horizontally scaled using docker swarm while maintaining order of events.

### Architecture

![Alt text](/images/mm_diagram.jpg?raw=true "Optional Title")

mm_dashboard - a static file server <br />
mm_api - a django based api to handle http requests socket connections from the dashboard <br />
celery_workers - celery workers responsible for processing events and storing in redis/postgres <br />
subscribe_events - consumes events from the RabbitMQ and distributes events to appropriate celery workers <br />
event_source - an api that receives events from registered mobile applications and publishes to RabbitMQ <br />



