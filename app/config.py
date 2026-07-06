import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    raise ValueError("RESEND_API_KEY environment variable not set")

CONTACT_ROUTING_EMAIL = os.getenv("CONTACT_ROUTING_EMAIL")
if not CONTACT_ROUTING_EMAIL:
    raise ValueError("CONTACT_ROUTING_EMAIL environment variable not set")

RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL")
if not RESEND_FROM_EMAIL:
    raise ValueError("RESEND_FROM_EMAIL environment variable not set")