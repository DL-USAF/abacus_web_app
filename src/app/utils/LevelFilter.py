from logging import Filter, INFO


class LevelFilter(Filter):
    def __init__(self, level_cutoff: int):
        self.level_cutoff = level_cutoff

    def filter(self, record):
        return record.levelno <= self.level_cutoff