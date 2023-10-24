from contextvars import ContextVar

REQUEST_ID_CONTEXT_VAR = ContextVar("REQUEST_ID_CONTEXT_VAR", default=None)
SERVICE_CONTEXT_VAR = ContextVar("SERVICE_CONTEXT_VAR", default=None)
