# gui_module.py
import cv2

from core.modules.base_service_module import BaseServiceModule, logger_config

module_logger = logger_config.get_logger(config_name="default")


# Module definition
class GuiModule(BaseServiceModule):
    def __init__(self, result_storage=None):
        super().__init__("GuiModule", result_storage=result_storage)
        self.methods = ModuleMethods()


# Module offered methods
class ModuleMethods:
    @staticmethod
    def execute_show_text(text="Hello"):
        module_logger.info(msg=f"Showing text => {text}")

    @staticmethod
    def execute_show_image(image):
        cv2.imshow('Fisheye Effect', image)
        wait_until_closed_or_keypress('Fisheye Effect')
        module_logger.info(msg=f"Displaying image")
        return True


# Module utils
def wait_until_closed_or_keypress(window_name='Fisheye Effect'):
    while True:
        key = cv2.waitKey(100)
        if key != -1:
            break
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
