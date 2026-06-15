from fastapi import FastAPI
from .routers import post, user, auth, vote
from .config import settings
from .rate_limiter import TokenBucketRateLimiter, rate_limit_request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
rate_limiter = TokenBucketRateLimiter(
    capacity=settings.rate_limit_capacity,
    refill_rate=settings.rate_limit_refill_rate,
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    return await rate_limit_request(
        request=request,
        call_next=call_next,
        limiter=rate_limiter,
        enabled=settings.rate_limit_enabled,
        exempt_paths=("/docs", "/redoc", "/openapi.json"),
    )


# SessionDep = Annotated[Session, Depends(get_db)]

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root() -> dict:
    return {"msg": "Hello This is a FastAPI project for a blog API"}
