from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import contact_router
from app.database import init_db
from app.models import contact_submission  # noqa: F401 — register table with SQLAlchemy


@asynccontextmanager
async def lifespan(app: FastAPI):
    # You can leave this empty or add other startup logic later
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(title="Moose OS Backend", lifespan=lifespan)

# Configure CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:3000",  # Example for a frontend running on localhost:3000
    "http://127.0.0.1:3000",  # Another common localhost address for the frontend
    "http://localhost:8000",  # Another common localhost address for the frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contact_router)


@app.get("/health")
def health():
    """Check that the service is running."""
    return {"status": "ok"}