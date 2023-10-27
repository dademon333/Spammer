from fastapi import APIRouter, Depends

from application.di.messages import (
    get_create_newsletter_use_case,
    get_create_message_use_case,
)
from application.use_cases.messages.create_message import CreateMessageUseCase
from application.use_cases.messages.create_newsletter import (
    CreateNewsletterUseCase,
)
from application.use_cases.messages.dto import (
    CreateMessageOutputDTO,
    CreateNewsletterInputDTO,
    CreateMessageInputDTO,
)
from application.utils.auth import check_auth
from application.web.views.common_responses import OkResponse

messages_router = APIRouter()


@messages_router.post("/newsletter", dependencies=[Depends(check_auth)])
async def create_newsletter(
    input_dto: CreateNewsletterInputDTO,
    use_case: CreateNewsletterUseCase = Depends(
        get_create_newsletter_use_case
    ),
) -> OkResponse:
    """Создание рассылки"""
    await use_case.execute(input_dto)
    return OkResponse()


@messages_router.post("", dependencies=[Depends(check_auth)])
async def create_message(
    input_dto: CreateMessageInputDTO,
    use_case: CreateMessageUseCase = Depends(get_create_message_use_case),
) -> CreateMessageOutputDTO:
    """Создание одиночных сообщений"""
    return await use_case.execute(input_dto)
