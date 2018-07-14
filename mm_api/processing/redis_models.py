from core.redisapp import redis
import json


class RedisDictModel(object):
    _db = redis
    expires = None
    default = {}

    def __init__(self, redis_id, *args, **kwargs):
        self.id = redis_id
        self.key = '%s:%s' % (self.__class__.__name__, self.id)
        self._data = None

    def exist(self):
        """
        Checks if key exist in redis
        """
        return self._db.exists(self.key)

    def __hash__(self):
        return hash(self.id)

    def __setitem__(self, key, value):
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
        Increment a value under a `key` by `val`
        """

        self._db.hincrby(self.key, key, val)

    def __delitem__(self, key):
        self._db.hdel(self.key, key)

    def __getitem__(self, key):
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
        """
        Returns a value under key or None
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


