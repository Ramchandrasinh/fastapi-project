from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.rate_limiter import TokenBucketRateLimiter, rate_limit_request


class FakeClock:
    def __init__(self) -> None:
        self.current = 0.0

    def __call__(self) -> float:
        return self.current

    def advance(self, seconds: float) -> None:
        self.current += seconds


def test_token_bucket_allows_burst_then_blocks():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0, now=clock)

    first = limiter.check("client-1")
    second = limiter.check("client-1")
    third = limiter.check("client-1")

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0
    assert third.allowed is False
    assert third.retry_after == 1


def test_token_bucket_refills_over_time():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0, now=clock)

    limiter.check("client-1")
    limiter.check("client-1")
    clock.advance(1.0)

    result = limiter.check("client-1")

    assert result.allowed is True
    assert result.remaining == 0


def test_rate_limit_middleware_returns_429_after_limit():
    limiter = TokenBucketRateLimiter(capacity=1, refill_rate=0.1)
    app = FastAPI()

    @app.middleware("http")
    async def rate_limit_middleware(request, call_next):
        return await rate_limit_request(request, call_next, limiter)

    @app.get("/")
    def root():
        return {"message": "ok"}

    client = TestClient(app)

    allowed = client.get("/")
    blocked = client.get("/")

    assert allowed.status_code == 200
    assert allowed.headers["X-RateLimit-Limit"] == "1"
    assert allowed.headers["X-RateLimit-Remaining"] == "0"
    assert blocked.status_code == 429
    assert blocked.json() == {"detail": "Rate limit exceeded"}
    assert blocked.headers["Retry-After"] == "10"
