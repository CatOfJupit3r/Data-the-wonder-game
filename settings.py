import os
from logging.config import dictConfig
import logging
import dotenv

dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_API_TOKEN")
AUTHOR_ID = int(os.getenv("ADMIN_ID"))

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s - %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s - %(message)s"
        },
    },
    'handlers': {
        "console": {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/infos.log',
            'mode' : 'a+',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)