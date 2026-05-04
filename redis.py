import redis.asyncio as aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

async def get_redis():
    redis = await aioredis.from_url(REDIS_URL)
    return redis