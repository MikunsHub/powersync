import logging


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)
