import resend
import logging
from .config import get_env

RESEND_API_KEY = get_env("RESEND_API_KEY", required=True)
EMAIL_FROM = get_env("EMAIL_FROM", required=True)
EMAIL_TO = get_env("EMAIL_TO", required=True)

resend.api_key = RESEND_API_KEY

def send_email(subject, html_body):
    try:
        resend.Emails.send({
            "from": EMAIL_FROM,
            "to": [EMAIL_TO],
            "subject": subject,
            "html": html_body
        })
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
