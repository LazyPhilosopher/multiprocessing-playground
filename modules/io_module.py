# io_module.py
import time
from pathlib import Path

import cv2

from modules.base_service_module import BaseServiceModule


# Module definition
class IoModule(BaseServiceModule):
    def __init__(self, result_storage=None):
        super().__init__("IoModule", process_count=1, result_storage=result_storage)  # Pass result_storage
        self.methods = ModuleMethods()


# Module offered methods
class ModuleMethods:
    @staticmethod
    def load_image(image_path: str | Path):
        time.sleep(2)
        return cv2.imread(image_path)


# Module utils
