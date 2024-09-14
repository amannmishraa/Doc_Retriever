import redis

cache = redis.Redis(host='localhost', port=6379, db=0)
def cache_results(user_id, results):
    cache.set(user_id, str(results), ex=3600) 

def get_cached_results(user_id):
    cached_data = cache.get(user_id)
    if cached_data:
        return eval(cached_data)
    return None
