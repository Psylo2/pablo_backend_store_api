from logging import StreamHandler, DEBUG

from application.core.logs.console.color_formatter import ColorFormatter


class CustomStreamHandler(StreamHandler):

    def __init__(self):
        super().__init__()
        self._color_log_formatter = ColorFormatter()
        self.setLevel(DEBUG)
        self.setFormatter(self._color_log_formatter)
