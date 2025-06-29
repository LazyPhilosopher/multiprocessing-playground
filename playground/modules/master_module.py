from enum import Enum

from playground.modules.gui_module import GuiModule
from playground.modules.math_module import MathModule


class Services(Enum):
    Math = 1
    GUI = 2


class MasterModule:
    def __init__(self):
        self.max_processes = 5
        self.services = {}

    def register_service(self, service: Services):
        instance = None
        match service:
            case Services.Math:
                instance = MathModule()
            case Services.GUI:
                instance = GuiModule()
            case _:
                # Raise Exception
                pass
        self.services[service] = instance
        instance.start()

    def shutdown(self):
        for service in self.services.values():
            service.stop()

    def get_service(self, service: Services):
        return self.services.get(service)