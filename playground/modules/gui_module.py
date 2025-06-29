from playground.modules.base_service_module import BaseServiceModule


class ModuleMethods:
    @staticmethod
    def execute_show_text(text="Hello"):
        print(f"Showing text: {text}")

    @staticmethod
    def execute_show_image(image_path="image.png"):
        print(f"Displaying image: {image_path}")


class GuiModule(BaseServiceModule):
    def __init__(self):
        super().__init__("GuiModule", process_count=1)
        self.methods = ModuleMethods()