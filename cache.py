import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_results(user_id, results):
    cache.set(user_id, str(results), ex=3600) 

def get_cached_results(user_id):
    return cache.get(user_id)