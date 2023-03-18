import logging

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail

logger = logging.getLogger(__name__)


def send_email(subject, content, recipient):
    message = Mail(
        from_email=settings.SENGRID_FROM_EMAIL,
        to_emails=recipient,
        subject=subject,
        html_content=Content("text/plain", content),
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        logger.error("Error sending email: ", e)
