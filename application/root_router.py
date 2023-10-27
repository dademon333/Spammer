from fastapi import APIRouter

from application.web.views.v1.messages import messages_router

root_router = APIRouter()

root_router.include_router(
    messages_router,
    prefix="/api/v1/messages",
    tags=["messages"],
)
