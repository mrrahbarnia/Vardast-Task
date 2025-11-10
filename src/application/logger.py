from pydantic import BaseModel


# In this config i wanted to store important logs with json format into files(for monitoring tools).
# And write not important logs into console.


class LogConfig(BaseModel):
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict[str, dict[str, str]] = {
        "console": {
            "format": '{"time":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s","function": "%(funcName)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
        "json": {
            "()": "pythonjsonlogger.json.JsonFormatter",
            "fmt": '{"time":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s","function": "%(funcName)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
    }
    handlers: dict[str, dict[str, str | int]] = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "console",
        },
        "json": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "WARNING",
            "formatter": "json",
            "filename": "./logs/app.log",
            "maxBytes": 5000000,  # 5 MB
            "encoding": "utf-8",
            "backupCount": 3,
        },
    }
