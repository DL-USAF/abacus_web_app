import logging

from .LevelFilter import LevelFilter


def create_logger(name: str, log_file: str):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        # Detailed file handler (WARNING, ERROR, CRITICAL)
        formatter = logging.Formatter(
            "\nTime:%(asctime)s\nLogger:%(name)s\nFile:%(filename)s:%(lineno)d\n"
            + "Log Level:%(levelname)s\nMessage:%(message)s\n")
        detailed_fh = logging.FileHandler(log_file)
        detailed_fh.setLevel(level=logging.WARNING)
        detailed_fh.setFormatter(formatter)
        logger.addHandler(detailed_fh)

        # Simple file handler (DEBUG, INFO)
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
        simple_fh = logging.FileHandler(log_file)
        simple_fh.setLevel(level=logging.DEBUG)
        simple_fh.setFormatter(formatter)
        level_filter = LevelFilter(logging.INFO)
        simple_fh.addFilter(level_filter)
        logger.addHandler(simple_fh)

        # Stream Handler (INFO, WARNING, ERROR, CRITICAL)
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
    return logger