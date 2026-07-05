from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import contact_router
from app.database import init_db
from app.models import contact_submission  # noqa: F401 — register table with SQLAlchemy


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Moose OS Backend", lifespan=lifespan)

app.include_router(contact_router)


@app.get("/health")
def health():
    """Check that the service is running."""
    return {"status": "ok"}