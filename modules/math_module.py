# math_module.py
import multiprocessing
from datetime import datetime

import cv2
import numpy as np

from modules.base_service_module import BaseServiceModule


# Module definition
class MathModule(BaseServiceModule):
    def __init__(self, result_storage=None):
        super().__init__("MathModule", process_count=1, result_storage=result_storage)
        self.methods = ModuleMethods()


# Module offered methods
class ModuleMethods:
    @staticmethod
    def execute_sum_calculation(x=1, y=2):
        print(f"[{datetime.now().strftime("%H:%M:%S")}][MathModule]: execute_sum_calculation => {x + y}")
        return x + y

    @staticmethod
    def execute_mul_calculation(x=10, y=20):
        import time
        time.sleep(5)
        print(f"[{datetime.now().strftime("%H:%M:%S")}][MathModule]: execute_mul_calculation => {x * y}")
        return x * y

    @staticmethod
    def fisheye_effect(image, strength=0.0005):
        height, width = image.shape[:2]
        map_y, map_x = np.indices((height, width), dtype=np.float32)
        x = map_x - width / 2
        y = map_y - height / 2
        r = np.sqrt(x ** 2 + y ** 2)

        theta = np.arctan(r * strength)
        scale = np.ones_like(r)

        mask = r != 0
        scale[mask] = theta[mask] / (r[mask] * strength)

        map_x = scale * x + width / 2
        map_y = scale * y + height / 2

        return cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)


# Module utils
