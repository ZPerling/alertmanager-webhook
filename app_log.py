import logging.config
from config import get_config


class MyLog:
    def __init__(self):
        config = {
            'version': 1,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)-10s :   %(message)s',
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple'
                },
                'log_to_file': {
                    'class': 'logging.FileHandler',
                    'filename': get_config().get('log').get('path'),
                    'level': 'DEBUG',
                    'formatter': 'simple'
                }
            },
            'loggers': {
                'console': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                },
                'log_to_file': {
                    'handlers': ['log_to_file'],
                    'level': 'DEBUG',
                }
            }
        }
        logging.config.dictConfig(config)
        self.log_to_file_logger = logging.getLogger('log_to_file')
        self.console_log_logger = logging.getLogger('console')
