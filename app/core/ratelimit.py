from upstash_ratelimit import Ratelimit, FixedWindow
from upstash_redis import Redis
from app.core.config import settings

redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
ratelimit = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=20, window=3600))