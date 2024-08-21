import datetime
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from textwrap import dedent

FORMAT_PATTERN = dedent("""
               [%(levelname)s] at %(asctime)s
               Module: %(module)s
               Function:%(funcName)s:%(lineno)d
               --------------------- Message ---------------------
               %(message)s
               ----------------------------------------------------
               """)


logging.basicConfig(level=logging.NOTSET, handlers=None)
TZ = datetime.timezone(datetime.timedelta(hours=8))


class ColoredFormatter(logging.Formatter):
    """A custom formatter to add colors to the log messages based on the log level.
    Only works for console logs(stdout, stderr) and not for file logs.
    """

    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True, *, defaults=None):
        super().__init__(
            fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults
        )
        self.formats: dict = {
            logging.DEBUG: self.blue + fmt + self.reset,
            logging.INFO: self.grey + fmt + self.reset,
            logging.WARNING: self.yellow + fmt + self.reset,
            logging.ERROR: self.red + fmt + self.reset,
            logging.CRITICAL: self.bold_red + fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_package_logger(
    package_name: str, file_level=logging.INFO, console_level=logging.DEBUG
) -> logging.Logger:
    """_summary_.

    Initialize the logger for the specified module.

    Args:
    ----
        package_name (str): The name of the package.
        file_level (int): The log level for the file handler.
        console_level (int): The log level for the console handler.

    """
    log_full_path = Path("logs") / Path(*(package_name.split(".")))

    log_full_path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)

    formatter = logging.Formatter(fmt=FORMAT_PATTERN)
    console_formatter = ColoredFormatter(fmt=FORMAT_PATTERN)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        filename=log_full_path.with_suffix(".log"),
        maxBytes=10 * 1024 * 1024,  # 10 MB
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    package_logger = logging.getLogger(package_name)
    package_logger.addHandler(console_handler)
    package_logger.addHandler(file_handler)
    return package_logger
