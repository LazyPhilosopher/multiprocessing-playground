# math_module.py
import cv2
import numpy as np

from core.modules.base_service_module import BaseServiceModule, logger_config

module_logger = logger_config.get_logger(config_name="default")


# Module definition
class MathModule(BaseServiceModule):
    def __init__(self, result_storage=None):
        super().__init__("MathModule", result_storage=result_storage)
        self.methods = ModuleMethods()


# Module offered methods
class ModuleMethods:
    @staticmethod
    def execute_sum_calculation(x: int | float = 1, y: int | float = 2):
        from core.utils import check_argument_types
        allowed_types = [float, int]
        args = {'x': x, 'y': y}
        passed, msg = check_argument_types(args=args, allowed_types=allowed_types)
        if not passed:
            return ValueError(msg)

        module_logger.info(f"execute_sum_calculation => {x + y}")
        return x + y

    @staticmethod
    def execute_mul_calculation(x: int | float = 10, y: int | float = 20):
        # check type of input
        from core.utils import check_argument_types
        allowed_types = [float, int, list]
        args = {'x': x, 'y': y}
        passed, msg = check_argument_types(args=args, allowed_types=allowed_types)
        if not passed:
            return ValueError(msg)

        import time
        time.sleep(10)
        module_logger.info(f"execute_mul_calculation => {x * y}")
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
