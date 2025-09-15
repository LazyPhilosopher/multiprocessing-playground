# main.py
import multiprocessing

from core.modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
from core.modules.master_module import MasterModule, Services, ModuleMethods as Macros, ResultStorage
from core.modules.math_module import MathModule, ModuleMethods as MathModuleMethods
from core.logger.logger import Logger
from core.struct.task import Task

logger_config = Logger()
main_logger = logger_config.get_logger(config_name="root")


if __name__ == "__main__":
    """Run several tasks simultaneously incorporating various modules in process."""
    from core.utils import wait_for_result
    multiprocessing.set_start_method('spawn')

    result_storage = ResultStorage()  # Shared dict to store results

    master = MasterModule(result_storage)   # Start Master module

    master.register_service([Services.Math, Services.GUI, Services.IO])     # Start modules necessary for task execution

    gui_service: GuiModule = master.get_service(Services.GUI)       # Get each module reference to send requests to them
    math_service: MathModule = master.get_service(Services.Math)
    math_service.set_max_threads(max_threads=15)

    # Complex macro execution - being executed in Master module's thread
    image_key = master.execute_macro(Macros.display_fisheye, {"image_path": "img/lena.png", "strength": 0.005})

    # Atomic tasks being requested by each module separately
    sum1_key = math_service.send_request(Task(func=MathModuleMethods.execute_sum_calculation, kwargs={"x": 2, "y": 3}, max_executions=20))
    mul1_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 5, "y": 7}))
    sum2_key = math_service.send_request(Task(func=MathModuleMethods.execute_sum_calculation, kwargs={"x": 2, "y": 3}, max_executions=20))

    mul2_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 1, "y": 9}))
    mul3_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 2, "y": 8}))
    mul4_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 3, "y": 7}))
    mul5_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 4, "y": 6}))
    mul6_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 5, "y": 5}))
    mul7_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 5, "y": 5}))
    mul8_key = math_service.send_request(Task(func=MathModuleMethods.execute_mul_calculation, kwargs={"x": 5, "y": 5}))
    math_keys = [sum1_key, sum2_key, mul1_key, mul2_key, mul3_key, mul4_key, mul5_key, mul6_key, mul7_key, mul8_key]

    gui_service.send_request(Task(func=GuiModuleMethods.execute_show_text))

    # Wait for atomic tasks to finish
    main_logger.debug(f"Await for multiplication task: {mul6_key}")
    wait_for_result(_key=mul8_key, result_storage=result_storage)

    # Display atomic tasks results
    main_logger.debug(f"Results from MathModule: {list(f"{key}: {result_storage.results[key]}" for key in math_keys)}")

    # Wait user to close GUI window
    main_logger.warning(f"Await for image closed: {image_key}")
    wait_for_result(_key=image_key, result_storage=result_storage, timeout_s=10)

    # Shutdown every module
    main_logger.debug(f"Execute shutdown.")
    master.shutdown()
