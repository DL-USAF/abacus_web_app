import logging


def create_logger(name: str, log_file: str):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        formatter = logging.Formatter(
            "Time:%(asctime)s\nLogger:%(name)s\nFile:%(filename)s:%(lineno)d\n"
            + "Log Level:%(levelname)s\nMessage:%(message)s\n")
        fh = logging.FileHandler(log_file)
        fh.setLevel(level=logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.propagate = False
    return logger