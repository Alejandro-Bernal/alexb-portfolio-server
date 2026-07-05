import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://moose:moose@localhost:5432/moose_os",
)

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
CONTACT_ROUTING_EMAIL = os.getenv("CONTACT_ROUTING_EMAIL", "contact@bernalforge.dev")
RESEND_FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL",
    "Bernal Forge <contact@bernalforge.dev>",
)