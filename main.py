import logging.config

from fastapi import FastAPI

from application.middlewares.request_id import RequestIDMiddleware
from application.root_router import root_router
from application.utils.log_config import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)

app = FastAPI()
app.include_router(root_router)
app.add_middleware(RequestIDMiddleware)
