import logging


def get_logger():
    logger = logging.getLogger('telegram')
    logger.setLevel(level=logging.INFO)
    logger.handlers = [logging.StreamHandler()]
    return logger
