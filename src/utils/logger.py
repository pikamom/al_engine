import logging
import sys

from colorlog import ColoredFormatter


class LoggerSetup:
    def __init__(self, log_file: str) -> None:
        logger = logging.getLogger()

        # add in console output handler + file handler
        console_output = logging.StreamHandler(sys.stderr)
        file_handler = logging.FileHandler(log_file)

        # formatter
        color_formatter = ColoredFormatter(
            "%(log_color)s[%(levelname)s][%(filename)s][%(asctime)s] %(reset)s%(white)s%(message)s", 
            datefmt="%m-%d %H:%M",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        )
        file_formatter=logging.Formatter(fmt="[%(levelname)s][%(filename)s][%(asctime)s] %(message)s", 
            datefmt="%m-%d %H:%M")

        console_output.setFormatter(color_formatter)
        file_handler.setFormatter(file_formatter)

        # add in console output handler
        logger.addHandler(console_output)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
