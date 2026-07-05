import asyncio
import logging

import resend

from app.config import CONTACT_ROUTING_EMAIL, RESEND_API_KEY, RESEND_FROM_EMAIL
from app.models.contact import ContactForm

logger = logging.getLogger(__name__)


class EmailSendError(Exception):
    pass


def _build_contact_email_html(form: ContactForm) -> str:
    return f"""
    <h2>New contact form submission</h2>
    <p><strong>Name:</strong> {form.name}</p>
    <p><strong>Email:</strong> {form.email}</p>
    <p><strong>Subject:</strong> {form.subject}</p>
    <p><strong>Message:</strong></p>
    <p>{form.message}</p>
    """


def _send_contact_email_sync(form: ContactForm) -> str:
    if not RESEND_API_KEY:
        raise EmailSendError("RESEND_API_KEY is not configured")

    resend.api_key = RESEND_API_KEY

    result = resend.Emails.send(
        {
            "from": RESEND_FROM_EMAIL,
            "to": [CONTACT_ROUTING_EMAIL],
            "reply_to": [str(form.email)],
            "subject": f"[Contact] {form.subject}",
            "html": _build_contact_email_html(form),
        }
    )

    email_id = result.get("id")
    if not email_id:
        raise EmailSendError("Resend did not return an email id")

    return email_id


async def send_contact_email(form: ContactForm) -> str:
    try:
        return await asyncio.to_thread(_send_contact_email_sync, form)
    except EmailSendError:
        raise
    except Exception as exc:
        logger.exception("Failed to send contact email via Resend")
        raise EmailSendError("Failed to send contact email") from exc