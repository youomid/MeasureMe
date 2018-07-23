# standard library imports
import json
import copy

# third party imports

# local imports
from core.redisapp import redis


class RedisDictModel(object):
    """
    Redis wrapper for dictionaries.
    """

    _db = redis
    expires = None
    default = {}

    def __init__(self, redis_id, *args, **kwargs):
        self.id = redis_id
        self.key = '%s:%s' % (self.__class__.__name__, self.id)
        self._data = None

    def exist(self):
        return self._db.exists(self.key)

    def __setitem__(self, key, value):
        """
        Update redis key in redis.

            Args:
                key: string containing the value to update
                value: updated int value

            Return:
                None
        """        

        if value is None:
            self._db.hdel(self.key, key)
            return
        try:
            value = int(value)
        except Exception:
            pass
        old_val = self.get(key)
        self._db.hset(self.key, key, json.dumps(value))
        if self._data is not None:
            self._data[key] = value

    def increment(self, key, val):
        """
        Increment a redis key by 1.

            Args:
                key: string containing the value to update
                val: updated int value

            Return:
                None
        """   

        self._db.hincrby(self.key, key, val)

    def __delitem__(self, key):
        self._db.hdel(self.key, key)

    def __getitem__(self, key):
        """
        Retrieve a redis key's value.

            Args:
                key: string containing the value to update

            Return:
                value: an int value
        """        

        value = self._data.get(key) if self._data else self._db.hget(self.key, key)
        if value is None and self.default.get(key) is None:
            raise KeyError('Key "%s" does not exist in %s' % (key, self.key))
        else:
            if value:
                if isinstance(value, int):
                    return value
                if isinstance(value, str):
                    try:
                        return int(value)
                    except ValueError:
                        return json.loads(value)
            else:
                return copy.copy(self.default.get(key))
            return value

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


