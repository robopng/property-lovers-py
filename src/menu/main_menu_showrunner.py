from src.controller import Controller


class MainMenuShowrunner(Controller):
    def __init__(self, renderer):
        super().__init__("NONE", "NONE", renderer)

    def begin(self):
        print("Made it!")
        self.return_code = "SIM"
