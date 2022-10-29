import os
from logging import DEBUG, Formatter
from logging.handlers import TimedRotatingFileHandler


from application.core.logs.base_log_formatter import BaseLogFormatter


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    default_folder_name = "logs/"

    def __init__(self, folder_name: str | None):
        self._folder_name = folder_name if folder_name else self.default_folder_name
        filename = self._folder_name + "Shoppa"

        try:
            super().__init__(filename=filename, when='midnight', interval=1, encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(self._folder_name)
            super().__init__(filename=filename, when='midnight', interval=1, encoding="utf-8")

        self.suffix = "%Y-%m-%d.log"
        self._log_formatter = Formatter(fmt=BaseLogFormatter.log_fmt, datefmt=BaseLogFormatter.log_datefmt)
        self.setLevel(DEBUG)
        self.setFormatter(self._log_formatter)
