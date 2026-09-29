import logging
from typing import Any, cast

redis_module: Any
try:
    import redis as _redis_module
except ImportError:
    redis_module = None
else:
    redis_module = _redis_module
logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self, url: str | None = None):
        self.client = (
            redis_module.Redis.from_url(
                url, socket_connect_timeout=1, socket_timeout=1, decode_responses=True
            )
            if url and redis_module
            else None
        )
        if url and redis_module is None:
            logger.warning(
                "Redis package is not installed; cache and rate limiting are disabled"
            )

    def get(self, key: str) -> str | None:
        if self.client is None:
            return None
        try:
            return cast(str | None, self.client.get(key))
        except Exception as exc:  # noqa: BLE001 - cache failures must not break requests
            logger.warning("Redis cache read unavailable: %s", exc)
            return None

    def ready(self) -> bool:
        if self.client is None:
            return False
        try:
            return bool(self.client.ping())
        except Exception:  # noqa: BLE001 - readiness reports Redis as unavailable
            return False

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        if self.client is None:
            return
        try:
            self.client.set(key, value, ex=ttl_seconds)
        except Exception as exc:  # noqa: BLE001 - cache failures must not break requests
            logger.warning("Redis cache write unavailable: %s", exc)

    def delete(self, key: str) -> None:
        if self.client is None:
            return
        try:
            self.client.delete(key)
        except Exception as exc:  # noqa: BLE001 - cache failures must not break requests
            logger.warning("Redis cache delete unavailable: %s", exc)

    def incr_with_expiry(self, key: str, ttl_seconds: int) -> int | None:
        if self.client is None:
            return None
        try:
            count = self.client.incr(key)
            if count == 1:
                self.client.expire(key, ttl_seconds)
            return int(count)
        except Exception as exc:  # noqa: BLE001 - rate-limit failures are fail-open
            logger.warning("Redis rate limit unavailable: %s", exc)
            return None
