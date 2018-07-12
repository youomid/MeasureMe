from core.redisapp import redis


class RedisModel(object):
    """
    This is a base redis model class. is used to represent redis key as object.
    """
    _db = redis
    expires = None

    def __init__(self, _id):
        self.id = _id
        self.key = '%s:%s' % (self.__class__.__name__, self.id)

    def exist(self):
        """
        Checks if key exist in redis
        """
        return self._db.exists(self.key)

    def delete(self):
        self._db.delete(self.key)

    def __hash__(self):
        return hash(self.id)


class RedisDictModel(RedisModel):

    default = {}

    def __init__(self, name, *args, **kwargs):
        super(RedisDictModel, self).__init__(name, *args, **kwargs)
        self._data = None

    def __setitem__(self, key, value):
        if value is None:
            self.db.hdel(self.key, key)
            return
        try:
            value = int(value)
        except Exception:
            pass
        old_val = self.get(key)
        self.db.hset(self.key, key, json.dumps(value))
        if self._data is not None:
            self._data[key] = value

        if key in self.attribute_change_hooks.keys():
            getattr(self, self.attribute_change_hooks[key])(key, value, old_val)

    def increment(self, key, val):
        """
        Increment a value under a `key` by `val`
        """
        if self._pipeline is not None:
            self._data[key] += int(val)
        self.db.hincrby(self.key, key, val)

    def __delitem__(self, key):
        self.db.hdel(self.key, key)

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
        Returns a value under key ot None
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


