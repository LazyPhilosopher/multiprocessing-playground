# main.py

import multiprocessing

from modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
from modules.master_module import MasterModule, Services, ModuleMethods as Macros, ResultStorage
from modules.math_module import MathModule, ModuleMethods as MathModuleMethods

if __name__ == "__main__":
    """Run several tasks simultaneously incorporating various modules in process."""
    from utils import wait_for_result

    from logger.logger import Logger
    logger_config = Logger()
    logger = logger_config.get_logger("master_module")

    multiprocessing.set_start_method('spawn')

    result_storage = ResultStorage()  # Shared dict to store results
    # result_event_dict = {} # dict with all upcoming result flags

    master = MasterModule(result_storage)   # Start Master module

    master.register_service([Services.Math, Services.GUI, Services.IO])     # Start modules necessary for task execution

    gui_service: GuiModule = master.get_service(Services.GUI)       # Get each module reference to send requests to them
    math_service: MathModule = master.get_service(Services.Math)

    # Complex macro execution - being executed in Master module's thread
    image_key = master.execute_macro(Macros.display_fisheye, {"image_path": "img/lena.png", "strength": 0.005})

    # Atomic tasks being requested by each module separately
    sum1_key = math_service.send_request(MathModuleMethods.execute_sum_calculation, {"x": 2, "y": 3})
    mul1_key = math_service.send_request(MathModuleMethods.execute_mul_calculation, {"x": 10, "y": 7})
    sum2_key = math_service.send_request(MathModuleMethods.execute_sum_calculation, {"x": 2, "y": 3})
    gui_service.send_request(GuiModuleMethods.execute_show_text)

    # Wait for atomic tasks to finish
    logger.info(f"Await for multiplication task: {mul1_key}")
    wait_for_result(_key=mul1_key, result_storage=result_storage, timeout_s=10)

    # Display atomic tasks results
    logger.info(f"Results from MathModule: {list(f"{key}: {result_storage.results[key]}" for key in [sum1_key, sum2_key, mul1_key])}")

    # Wait user to close GUI window
    logger.info(f"Await for image closed: {image_key}")
    wait_for_result(_key=image_key, result_storage=result_storage, timeout_s=10)

    # Shutdown every module
    master.shutdown()
