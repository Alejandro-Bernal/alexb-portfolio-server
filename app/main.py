from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.api.routes import inquiries_router
from app.limiter import limiter
from app.logging_config import setup_logging


# This is our new, correctly typed handler
async def rate_limit_exceeded_handler(request: Request, exc: Exception):
    """
    Custom handler for when a rate limit is exceeded.
    """
    # This check proves to the type checker that exc is a RateLimitExceeded instance
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": f"Rate limit exceeded: {exc.detail}"},
        )
    # Fallback for any other unexpected case
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    # You can leave this empty or add other startup logic later
    setup_logging()
    yield


app = FastAPI(
    title="Moose-OS Backend",
    description="API for Moose-OS portfolio website.",
    version="0.1.0",
    lifespan=lifespan, # Use the lifespan manager
)


# 2. Add the limiter to the app's state and attach the exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# Configure CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://localhost:5173",      # ← Add this (your Vite dev server)
    "http://127.0.0.1:5173",      # ← And this
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(inquiries_router)


@app.get("/health")
def health():
    """Check that the service is running."""
    return {"status": "ok"}