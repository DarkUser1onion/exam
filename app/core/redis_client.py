import redis
from app.config import REDIS_URL

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
            _redis_client.ping()
        except Exception:
            _redis_client = None
    return _redis_client
