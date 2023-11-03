import json
import logging

import aiohttp

from application.config import WAPICO_ACCESS_TOKEN

logger = logging.getLogger(__name__)


class WapicoClient:
    @staticmethod
    async def send_message(
        phone_number: str, message: str, instance_id: str
    ) -> dict | None:
        url = (
            "https://biz.wapico.ru/api/task_add.php?"
            f"access_token={WAPICO_ACCESS_TOKEN}"
            f"&number={phone_number}"
            f"&type=text"
            f"&message={message}"
            f"&instance_id={instance_id}"
            f"&timeout=0"
        )
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.post(url)
                return json.loads(await response.text())
            except aiohttp.ClientError:
                logger.warning("Ошибка подключения к wapico")
                return None
            except json.decoder.JSONDecodeError:
                logger.warning("Wapico вернул ответ не в формате json")
                return None
            except Exception:
                logger.exception(
                    "Неизвестная ошибка при запросе к wapico",
                    extra={
                        "phone_number": phone_number,
                        "message_text": message,
                        "instance_id": instance_id,
                    },
                )
                return None
