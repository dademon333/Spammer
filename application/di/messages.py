from fastapi import Depends

from application.di.repositories import get_message_repository
from application.use_cases.messages.create_message import CreateMessageUseCase
from application.use_cases.messages.create_newsletter import (
    CreateNewsletterUseCase,
)


def get_create_message_use_case(
    messages_repository=Depends(get_message_repository),
) -> CreateMessageUseCase:
    return CreateMessageUseCase(
        message_repository=messages_repository,
    )


def get_create_newsletter_use_case(
    messages_repository=Depends(get_message_repository),
) -> CreateNewsletterUseCase:
    return CreateNewsletterUseCase(
        message_repository=messages_repository,
    )
