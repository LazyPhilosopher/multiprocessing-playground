from playground.modules.base_service_module import BaseServiceModule


class ModuleMethods:
    @staticmethod
    def execute_short_calculation(x=1, y=2):
        print(x + y)
        return x + y

    @staticmethod
    def execute_long_calculation(x=10, y=20):
        import time
        time.sleep(5)
        print(x * y)
        return x * y


class MathModule(BaseServiceModule):
    def __init__(self):
        super().__init__("MathModule", process_count=1)
        self.methods = ModuleMethods()