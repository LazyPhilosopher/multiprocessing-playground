# logger.py

import logging
import logging.config
import colorlog
import os
import sys

class Logger:
    instance_dict = {}

    def __init__(self, config_file='logger/logger.config'):
        # Load logging configuration from the specified file
        if os.path.exists(config_file):
            logging.config.fileConfig(config_file)
        else:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        # Set up color formatter
        self.setup_color_formatter()

    def setup_color_formatter(self):
        # Create a console handler with a color formatter
        handler = logging.StreamHandler(sys.stdout)

        # Define ANSI escape codes for colors
        RED = '\033[91m'
        GREEN = '\033[92m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

        formatter = colorlog.ColoredFormatter(
            fmt=(
                f"[{RED}%(asctime)s{RESET}]"
                f"[{GREEN}%(name)s{RESET}]:"
                f"{WHITE}%(message)s{RESET}"
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

        handler.setFormatter(formatter)

        # Add handler to root logger
        logging.getLogger().handlers = [handler]

    def get_logger(self, name):
        # Get a logger with the specified name
        logger_instance = logging.getLogger(name)
        Logger.instance_dict[name] = logger_instance
        return logger_instance
