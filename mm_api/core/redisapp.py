import redis

from django.conf import settings

redis = redis.StrictRedis(**settings.REDIS_DATASTORE)
