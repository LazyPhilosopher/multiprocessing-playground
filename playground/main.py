
import multiprocessing

from modules.master_module import MasterModule, Services
from playground.modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
from playground.modules.math_module import MathModule, ModuleMethods as MathModuleMethods

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # или 'fork' на Unix

    master = MasterModule()

    master.register_service(Services.Math)
    master.register_service(Services.GUI)

    # создаём очередь для получения ответа
    response_queue = multiprocessing.Queue()

    # вызываем метод с возвратом результата
    math_service: MathModule = master.get_service(Services.Math)
    gui_service: GuiModule = master.get_service(Services.GUI)
    gui_service.send_request(GuiModuleMethods.execute_show_image)
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y": 3})
    math_service.send_request(MathModuleMethods.execute_long_calculation, {"x": 10, "y":7})
    math_service.send_request(MathModuleMethods.execute_short_calculation, {"x": 2, "y":3})
    gui_service.send_request(GuiModuleMethods.execute_show_text)

    result = response_queue.get()
    print("Result from MathModule:", result)

    # вызов GUI без ожидания ответа
    # gui.send_request(gui.methods.execute_show_text, {"text": "Computation done!"})

    master.shutdown()