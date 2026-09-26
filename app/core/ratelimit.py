import logging

from upstash_ratelimit import Ratelimit, FixedWindow
from upstash_redis import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
ratelimit = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=20, window=3600))


def is_allowed(identifier: str) -> bool:
    """Check the fixed-window limit for `identifier`, failing open on errors.

    The limiter lives behind Upstash's REST API, so a DNS/network/Upstash outage
    (or an expired free-tier database) must not turn every /ask/stream request
    into a 500. When the check cannot be performed, the request is allowed and
    the failure is logged.
    """
    try:
        return ratelimit.limit(identifier).allowed
    except Exception as exc:
        logger.warning("Rate limit check failed for %s, allowing request: %s", identifier, exc)
        return True