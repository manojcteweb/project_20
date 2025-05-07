import logging


def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured.")
    return logger
