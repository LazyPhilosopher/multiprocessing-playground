# master_module.py
import uuid
from pathlib import Path

import cv2
import numpy as np
import threading

from enum import Enum
from modules.gui_module import GuiModule
from modules.io_module import IoModule
from modules.math_module import MathModule


class Services(Enum):
    Math    = 1
    GUI     = 2
    IO      = 3


# Module definition
class MasterModule:
    def __init__(self, result_storage):
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
            t = threading.Thread(target=macro, kwargs={"master_module": self, "result_key": key,  })
        t.start()
        return key

    def shutdown(self):
        for service in self.services.values():
            service.stop()

    def get_service(self, service: Services):
        return self.services.get(service)

    def get_result(self, item_key: str):
        return self.result_storage.pop(item_key)


# Module offered methods
class ModuleMethods:
    @staticmethod
    def display_fisheye(master_module, result_key: str, image_path: str | Path):
        from modules.gui_module import GuiModule, ModuleMethods as GuiModuleMethods
        from modules.math_module import MathModule, ModuleMethods as MathModuleMethods
        from modules.io_module import IoModule, ModuleMethods as IoModuleMethods

        gui_service: GuiModule = master_module.get_service(Services.GUI)
        math_service: MathModule = master_module.get_service(Services.Math)
        io_module: IoModule = master_module.get_service(Services.IO)

        # Request image load and wait for execution
        print("Request image load and wait for execution")
        img_key = io_module.send_request(IoModuleMethods.load_image, {"image_path": image_path})
        while img_key not in master_module.result_storage:
            pass
        image = master_module.get_result(item_key=img_key)

        # Request for image distortion and wait for execution
        print("Request for image distortion and wait for execution")
        distorded_key = math_service.send_request(MathModuleMethods.fisheye_effect, {"image": image, "strength": 0.01})
        while distorded_key not in master_module.result_storage:
            pass
        image = master_module.get_result(item_key=distorded_key)

        # Request image display and wait for execution
        print("Request image display and wait for execution")
        windows_closed_key = gui_service.send_request(GuiModuleMethods.execute_show_image, {"image": image})
        print(windows_closed_key)
        while windows_closed_key not in master_module.result_storage:
            pass

        print(f"Put True to {result_key}")
        master_module.result_storage[result_key] = True


# Module utils
