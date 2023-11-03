import json
import re

from aioresponses import aioresponses

from application.external_sources.wapico.wapico import WapicoClient


async def test_successful_request(mock_aioresponse: aioresponses):
    mock_aioresponse.post(
        url=re.compile(r"https://biz\.wapico\.ru/api/task_add\.php.+"),
        body=json.dumps({"status": "success", "data": {"task_id": "449653"}}),
        headers={"Content-Type": "text/html; charset=UTF-8"},
    )
    result = await WapicoClient.send_message(
        phone_number="79826661122",
        message="Hello, dear",
        instance_id="642D8BD6EEA12",
    )
    assert isinstance(result, dict)
    assert result["status"] == "success"
