# main.py
import multiprocessing as mp
mp.set_start_method('spawn')


from modules.master_module import MasterModule, Services, ModuleMethods as Macros, await_result_by_key
from modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
from modules.math_module import MathModule, ModuleMethods as MathModuleMethods


if __name__ == "__main__":
    """Run several tasks simultaneously incorporating various modules in process."""
    master = MasterModule()   # Start Master module

    master.register_service([Services.Math, Services.GUI, Services.IO])     # Start modules necessary for task execution

    gui_service: GuiModule = master.get_service(Services.GUI)       # Get each module reference to send requests to them
    math_service: MathModule = master.get_service(Services.Math)

    # Complex macro execution - being executed in Master module's thread
    image_key = master.execute_macro(Macros.display_fisheye, {"image_path": "img/lena.png", "strength": 0.005})

    # Atomic tasks being requested by each module separately
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y": 3})
    key = math_service.send_request(MathModuleMethods.execute_long_calculation, {"x": 10, "y": 7})
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y": 3})
    gui_service.send_request(GuiModuleMethods.execute_show_text)

    # Wait for atomic tasks to finish
    result_arrived = await_result_by_key(result_key=key, timeout_s=15)

    # Display atomic tasks results
    if result_arrived:
        print("Results from MathModule:", list(master.result_storage.items()))
    else:
        print("Error while waiting for MathModule atomic tasks execution.")

    # Display atomic tasks results
    print("Results from MathModule:", list(master.result_storage.items()))

    # Wait user to close GUI window
    print(f"Await for image closed: {key}")
    while image_key not in master.result_storage:
        pass

    # Shutdown every module
    master.shutdown()
