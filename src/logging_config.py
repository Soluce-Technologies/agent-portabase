import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'fancy': {
            'format': (
                '\033[1;34m%(asctime)s\033[0m | '        
                '\033[1;36m%(name)s\033[0m | '         
                '%(levelname_icon)s %(levelname)s | '  
                '\033[1;37m%(message)s\033[0m'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'fancy',
        },
    },
    'loggers': {
        'celery.beat': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'agent_logger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}


class FancyFormatter(logging.Formatter):
    """Custom formatter to add icons for log levels."""
    LEVEL_ICONS = {
        'DEBUG': '🐛',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }

    def format(self, record):
        record.levelname_icon = self.LEVEL_ICONS.get(record.levelname, '')
        return super().format(record)


def setup_logging():
    dictConfig(LOGGING_CONFIG)
    for logger_name, logger_config in LOGGING_CONFIG['loggers'].items():
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            if isinstance(handler.formatter, logging.Formatter):
                handler.setFormatter(FancyFormatter(handler.formatter._fmt))

