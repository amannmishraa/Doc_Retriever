from cachetools import TTLCache

class Cache:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=300)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
