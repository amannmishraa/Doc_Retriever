import aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def increment_user_requests(user_id: str):
    key = f"user_requests:{user_id}"
    await redis.incr(key)
    await redis.expire(key, 3600)  

async def get_user_requests(user_id: str) -> int:
    key = f"user_requests:{user_id}"
    count = await redis.get(key)
    return int(count) if count else 0
