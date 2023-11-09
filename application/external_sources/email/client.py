from email.message import EmailMessage
from email.mime.text import MIMEText

import aiosmtplib

from application.config import (
    EMAIL_ADDRESS,
    EMAIL_SERVER_URL,
    EMAIL_SERVER_PORT,
)


class EmailClient:
    """https://pypi.org/project/aiosmtplib/"""

    @staticmethod
    async def send_message(
        to: str,
        subject: str,
        message: str,
    ):
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(MIMEText(message).as_string())
        await aiosmtplib.send(
            msg, hostname=EMAIL_SERVER_URL, port=EMAIL_SERVER_PORT
        )
