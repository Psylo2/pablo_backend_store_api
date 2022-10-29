from logging import Formatter, LogRecord

from application.core.logs.base_log_formatter import BaseLogFormatter

class ColorFormatter(Formatter):
    log_level_color_mapper = {
        'DEBUG': 37,  # white
        'INFO': 36,  # cyan
        'WARNING': 33,  # yellow
        'ERROR': 31,  # red
        'CRITICAL': 41,  # white on red bg
    }

    PREFIX = '\033['
    SUFFIX = '\033[0m'

    def __init__(self):
        super().__init__(fmt=BaseLogFormatter.log_fmt, datefmt=BaseLogFormatter.log_datefmt)

    def format(self, record: LogRecord) -> str:
        level_name = record.levelname
        level_color_value = self.log_level_color_mapper.get(level_name, 37)
        colored_level_name = f'{self.PREFIX}{level_color_value}m{level_name}{self.SUFFIX}'
        record.levelname = colored_level_name
        return super().format(record=record)
