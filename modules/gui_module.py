# gui_module.py
import cv2

from modules.base_service_module import BaseServiceModule


# Module definition
class GuiModule(BaseServiceModule):
    def __init__(self, result_storage=None):
        super().__init__("GuiModule", process_count=1, result_storage=result_storage)  # Pass result_storage
        self.methods = ModuleMethods()


# Module offered methods
class ModuleMethods:
    @staticmethod
    def execute_show_text(text="Hello"):
        print(f"Showing text: {text}")

    @staticmethod
    def execute_show_image(image):
        cv2.imshow('Fisheye Effect', image)
        wait_until_closed_or_keypress('Fisheye Effect')
        print(f"Displaying image")
        return True


# Module utils
def wait_until_closed_or_keypress(window_name='Fisheye Effect'):
    while True:
        key = cv2.waitKey(100)
        if key != -1:
            break
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
