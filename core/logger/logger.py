# logger.py

import logging
import logging.config
import colorlog
import os
import sys


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Logger:

    def __init__(self, config_file='core/logger/logger.config'):
        # Load logging configuration from the specified file
        if os.path.exists(config_file):
            logging.config.fileConfig(config_file)
        else:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        self.setup_color_formatter()

    def setup_color_formatter(self):
        # Define ANSI escape codes for colors
        BLACK = '\033[90m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        DEFAULT = '\033[99m'
        RESET = '\033[0m'

        stdout_formatter = colorlog.ColoredFormatter(
            fmt=(
                f"[{MAGENTA}%(asctime)s{RESET}]"
                f"[{BLUE}%(module)s{RESET}]:"
                f"%(log_color)s%(message)s{RESET}"
                # f"{WHITE}%(message)s{RESET}"
            ),
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'green',
                'INFO': 'light_white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        file_formatter = colorlog.ColoredFormatter(
            fmt=(
                f"[%(asctime)s]"
                f"[%(module)s]:\t"
                f"%(message)s"
            ),
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        # Create a console handler with a color formatter
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(stdout_formatter)

        # Create a log file handler with a color formatter
        file_handler = logging.FileHandler('logs.txt')
        file_handler.setFormatter(file_formatter)

        # Add handler to root logger
        logging.getLogger().handlers = [stdout_handler, file_handler]

    def get_logger(self, config_name):
        logger_instance = logging.getLogger(config_name)
        return logger_instance
