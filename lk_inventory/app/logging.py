import logging.config


def init_logging(level='INFO'):
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            '': {
                'level': level,
            }
        }
    }
    logging.config.dictConfig(logging_config)
