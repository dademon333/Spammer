import logging

import aiohttp

from application.config import SMSC_LOGIN, SMSC_PASSWORD
from application.external_sources.smsc.dto import (
    SMSCSuccessfulResponse,
    SMSCErrorResponse,
)

logger = logging.getLogger(__name__)


class SMSCClient:
    @staticmethod
    async def send_message(
        phone_number: str, message: str
    ) -> SMSCSuccessfulResponse | SMSCErrorResponse:
        unknown_error_response = SMSCErrorResponse(
            error="Неизвестная ошибка от smsc",
            error_code="unknown_error",
        )

        async with aiohttp.ClientSession() as session:
            try:
                response = await session.post(
                    "https://smsc.ru/rest/send/",
                    json={
                        "login": SMSC_LOGIN,
                        "psw": SMSC_PASSWORD,
                        "phones": phone_number,
                        "mes": message,
                        "fmt": "3",
                        "cost": "3",
                    },
                )
                response_json = await response.json()
            except aiohttp.ClientError:
                logger.warning("Ошибка подключения к smsc")
                return unknown_error_response
            except Exception:
                logger.exception(
                    "Неизвестная ошибка при запросе к smsc",
                    extra={
                        "phone_number": phone_number,
                        "message_text": message,
                    },
                )
                return unknown_error_response

            if "cnt" in response_json:
                return SMSCSuccessfulResponse(**response_json)
            if "error" in response_json:
                return SMSCErrorResponse(**response_json)

            logger.warning(
                "Неизвестный ответ от smsc",
                extra={
                    "phone_number": phone_number,
                    "message_text": message,
                    "response": response_json,
                },
            )
            return unknown_error_response
