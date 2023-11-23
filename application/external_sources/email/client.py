from email.message import EmailMessage
from email.utils import formataddr

import aiosmtplib

from application.config import (
    EMAIL_ADDRESS,
    EMAIL_SERVER_URL,
    EMAIL_SERVER_PORT,
    EMAIL_PASSWORD,
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
        msg["From"] = formataddr(("Service Name", EMAIL_ADDRESS))
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(message)
        await aiosmtplib.send(
            msg,
            hostname=EMAIL_SERVER_URL,
            port=EMAIL_SERVER_PORT,
            username=EMAIL_ADDRESS,
            password=EMAIL_PASSWORD,
            use_tls=True,
            timeout=15,
        )
