# master_module.py
import multiprocessing
import threading
import uuid
from enum import Enum
from pathlib import Path

from core.modules.gui_module import GuiModule
from core.modules.io_module import IoModule
from core.modules.math_module import MathModule

from core.modules.base_service_module import logger_config
from core.struct.task import Task

module_logger = logger_config.get_logger("default")


class Services(Enum):
    Math = 1
    GUI = 2
    IO = 3


class ResultStorage:
    def __init__(self):
        manager = multiprocessing.Manager()
        self.results = manager.dict()
        self.new_item_condition = multiprocessing.Condition()

    def put_result(self, _key, _value):
        self.results[_key] = _value
        with self.new_item_condition:
            self.new_item_condition.notify_all()
            module_logger.info(f"Notify for putting result for {_key}")


# Module definition
class MasterModule:
    def __init__(self, result_storage: ResultStorage):
        self.max_processes = 5
        self.services = {}
        self.result_storage = result_storage
        self.macros = ModuleMethods()

    def register_service(self, service: Services | list):
        if isinstance(service, list):
            for s in service:
                self.register_service(s)
            return

        instance = None
        match service:
            case Services.Math:
                instance = MathModule(result_storage=self.result_storage)
            case Services.GUI:
                instance = GuiModule(result_storage=self.result_storage)
            case Services.IO:
                instance = IoModule(result_storage=self.result_storage)
            case _:
                # Raise Exception
                pass
        self.services[service] = instance
        instance.start()

    def execute_macro(self, macro, arguments: dict | None):
        key = uuid.uuid4()
        if arguments:
            t = threading.Thread(target=macro, kwargs={"master_module": self, "result_key": key, **arguments})
        else:
            t = threading.Thread(target=macro, kwargs={"master_module": self, "result_key": key, })
        t.start()
        return key

    def shutdown(self):
        for service in self.services.values():
            service.stop()

    def get_service(self, service: Services):
        return self.services.get(service)

    def get_result(self, item_key: str):
        return self.result_storage.results.pop(item_key)


# Module offered methods
class ModuleMethods:
    @staticmethod
    def display_fisheye(master_module, result_key: str, image_path: str | Path, strength: float):
        from core.utils import wait_for_result

        from core.modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
        from core.modules.math_module import MathModule, ModuleMethods as MathModuleMethods
        from core.modules.io_module import IoModule, ModuleMethods as IoModuleMethods

        gui_service: GuiModule = master_module.get_service(Services.GUI)
        math_service: MathModule = master_module.get_service(Services.Math)
        io_module: IoModule = master_module.get_service(Services.IO)

        # Request image load and wait for execution
        img_key = io_module.send_request(Task(func=IoModuleMethods.load_image, kwargs={"image_path": image_path}))
        module_logger.info(f"Request image load and wait for execution: {img_key}")
        # while img_key not in master_module.result_storage.results:
        #     pass
        wait_for_result(_key=img_key, result_storage=master_module.result_storage, timeout_s=600)
        image = master_module.get_result(item_key=img_key)

        # Request for image distortion and wait for execution
        distorded_key = math_service.send_request(Task(func=MathModuleMethods.fisheye_effect, kwargs={"image": image, "strength": strength}))

        module_logger.info(f"Request for image distortion and wait for execution: {distorded_key}")
        while distorded_key not in master_module.result_storage.results:
            pass
        wait_for_result(_key=distorded_key, result_storage=master_module.result_storage, timeout_s=600)
        image = master_module.get_result(item_key=distorded_key)

        # Request image display and wait for execution
        windows_closed_key = gui_service.send_request(Task(func=GuiModuleMethods.execute_show_image, kwargs={"image": image}))
        module_logger.info(f"Request image display and wait for execution: {windows_closed_key}")
        # while windows_closed_key not in master_module.result_storage.results:
        #     pass
        wait_for_result(_key=windows_closed_key, result_storage=master_module.result_storage, timeout_s=600)

        module_logger.info(f"Window closed")
        master_module.result_storage.put_result(_key=result_key, _value=True)


# Module utils
