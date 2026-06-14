import math
import threading
import time
from dataclasses import dataclass
from typing import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse


@dataclass
class TokenBucket:
    tokens: float
    updated_at: float


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after: int


class TokenBucketRateLimiter:
    """Thread-safe in-memory token bucket rate limiter."""

    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        now: Callable[[], float] = time.monotonic,
    ) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be greater than 0")

        self.capacity = capacity
        self.refill_rate = refill_rate
        self._now = now
        self._buckets: dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def check(self, key: str) -> RateLimitResult:
        with self._lock:
            now = self._now()
            bucket = self._buckets.get(key)

            if bucket is None:
                bucket = TokenBucket(tokens=float(self.capacity), updated_at=now)
                self._buckets[key] = bucket

            elapsed = max(0.0, now - bucket.updated_at)
            bucket.tokens = min(
                float(self.capacity),
                bucket.tokens + elapsed * self.refill_rate,
            )
            bucket.updated_at = now

            if bucket.tokens >= 1.0:
                bucket.tokens -= 1.0
                return RateLimitResult(
                    allowed=True,
                    limit=self.capacity,
                    remaining=math.floor(bucket.tokens),
                    retry_after=0,
                )

            retry_after = math.ceil((1.0 - bucket.tokens) / self.refill_rate)
            return RateLimitResult(
                allowed=False,
                limit=self.capacity,
                remaining=0,
                retry_after=max(1, retry_after),
            )

    def reset(self) -> None:
        with self._lock:
            self._buckets.clear()


def get_client_key(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    if request.client:
        return request.client.host
    return "anonymous"


def add_rate_limit_headers(response: Response, result: RateLimitResult) -> None:
    response.headers["X-RateLimit-Limit"] = str(result.limit)
    response.headers["X-RateLimit-Remaining"] = str(result.remaining)
    if result.retry_after:
        response.headers["Retry-After"] = str(result.retry_after)


async def rate_limit_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
    limiter: TokenBucketRateLimiter,
    enabled: bool = True,
    exempt_paths: tuple[str, ...] = (),
) -> Response:
    if not enabled or request.url.path in exempt_paths:
        return await call_next(request)

    result = limiter.check(get_client_key(request))
    if not result.allowed:
        response = JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded"},
        )
        add_rate_limit_headers(response, result)
        return response

    response = await call_next(request)
    add_rate_limit_headers(response, result)
    return response
