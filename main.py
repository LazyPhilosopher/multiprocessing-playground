# main.py

import multiprocessing

from modules.master_module import MasterModule, Services, ModuleMethods as Macros
from modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
from modules.math_module import MathModule, ModuleMethods as MathModuleMethods


if __name__ == "__main__":
    """Run several tasks simultaneously incorporating various modules in process."""
    multiprocessing.set_start_method('spawn')
    manager = multiprocessing.Manager()
    result_storage = manager.dict()  # Shared dict to store results

    master = MasterModule(result_storage)   # Start Master module

    master.register_service([Services.Math, Services.GUI, Services.IO])     # Start modules necessary for task execution

    gui_service: GuiModule = master.get_service(Services.GUI)       # Get each module reference to send requests to them
    math_service: MathModule = master.get_service(Services.Math)

    # Complex macro execution - being executed in Master module's thread
    image_key = master.execute_macro(Macros.display_fisheye, {"image_path": "img/lena.png"})

    # Atomic tasks being requested by each module separately
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y": 3})
    key = math_service.send_request(MathModuleMethods.execute_long_calculation, {"x": 10, "y": 7})
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y": 3})
    gui_service.send_request(GuiModuleMethods.execute_show_text)

    # Wait for atomic tasks to finish
    print(f"Await for atomic tasks: {key}")
    while key not in result_storage:
        pass

    # Display atomic tasks results
    print("Results from MathModule:", list(result_storage.items()))

    # Wait user to close GUI window
    print(f"Await for image closed: {key}")
    while image_key not in result_storage:
        pass

    # Shutdown every module
    master.shutdown()
