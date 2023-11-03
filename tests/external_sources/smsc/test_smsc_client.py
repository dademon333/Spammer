import json

from aioresponses import aioresponses

from application.external_sources.smsc.client import SMSCClient
from application.external_sources.smsc.dto import (
    SMSCSuccessfulResponse,
    SMSCErrorResponse,
)


async def test_successful_request(mock_aioresponse: aioresponses):
    mock_aioresponse.post(
        "https://smsc.ru/rest/send/",
        body=json.dumps(
            {"id": 869324, "cnt": 1, "cost": 4.20, "balance": 1684.30}
        ),
    )

    result = await SMSCClient.send_message(
        phone_number="79826661122", message="Hello, dear"
    )
    assert isinstance(result, SMSCSuccessfulResponse)
    assert result.id == 869324
    assert result.balance == 1684.30


async def test_not_enough_money(mock_aioresponse: aioresponses):
    mock_aioresponse.post(
        "https://smsc.ru/rest/send/",
        body=json.dumps(
            {
                "id": 869324,
                "error": "Недостаточно средств на счете Клиента",
                "error_code": 3,
            },
            ensure_ascii=False,
        ),
    )

    result = await SMSCClient.send_message(
        phone_number="79826661122", message="Hello, dear"
    )
    assert isinstance(result, SMSCErrorResponse)
    assert result.error_code == "3"


async def test_500_response(mock_aioresponse: aioresponses):
    mock_aioresponse.post(
        "https://smsc.ru/rest/send/", body="unknown_server_error", status=500
    )

    result = await SMSCClient.send_message(
        phone_number="79826661122", message="Hello, dear"
    )
    assert isinstance(result, SMSCErrorResponse)
    assert result.error_code == "unknown_error"
