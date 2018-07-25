# standard library imports

# local imports

# third party imports
from django.conf import settings
import redis


redis = redis.StrictRedis(**settings.REDIS_DATASTORE)
