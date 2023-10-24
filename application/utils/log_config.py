import json
import logging
from datetime import datetime

from application.utils.contexts import REQUEST_ID_CONTEXT_VAR


class JSONFormatter(logging.Formatter):
    """Логгер, позволяющий писать логи в json формате."""

    def format(self, record: logging.LogRecord):
        json_message = {
            "@timestamp": f"{datetime.utcnow().isoformat()}Z",
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "x-request-id": REQUEST_ID_CONTEXT_VAR.get(None),
            "extra": record.__dict__.get("extra", {}),
        }

        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            json_message["exception"] = record.exc_text
        if record.stack_info:
            json_message["stack_trace"] = self.formatStack(record.stack_info)
        return json.dumps(json_message, ensure_ascii=False)


LOG_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"()": "application.utils.log_config.JSONFormatter"}
    },
    "handlers": {
        "default": {"class": "logging.StreamHandler", "formatter": "default"}
    },
    "loggers": {"": {"level": "INFO", "handlers": ["default"]}},
}
