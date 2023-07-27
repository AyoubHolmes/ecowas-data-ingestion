import logging
import sys

from colorama import init, Fore, Style

init()


class CustomLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - Data_backend - %(name)s - %(levelname)s - %(message)s"
        )

        # log lower levels to stdout
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
        stdout_handler.setFormatter(formatter)
        self.addHandler(stdout_handler)

        # log higher levels to stderr (red)
        stderr_handler = logging.StreamHandler(stream=sys.stderr)
        stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)
        stderr_handler.setFormatter(formatter)
        self.addHandler(stderr_handler)

    def _log_with_color(self, color, level, message):
        record = self.makeRecord(self.name, level, "", 0, message, None, None)
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        self.handle(record)

    def debug(self, message):
        self._log_with_color(Fore.CYAN, logging.DEBUG, message)

    def info(self, message):
        self._log_with_color(Fore.GREEN, logging.INFO, message)

    def warning(self, message):
        self._log_with_color(Fore.YELLOW, logging.WARNING, message)

    def error(self, message):
        self._log_with_color(Fore.RED, logging.ERROR, message)

    def critical(self, message):
        self._log_with_color(Style.BRIGHT + Fore.RED, logging.CRITICAL, message)
