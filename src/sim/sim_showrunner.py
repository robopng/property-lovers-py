from src.controller import Controller


class SimShowrunner(Controller):
    def __init__(self, renderer):
        super().__init__("NONE", "NONE", renderer)

    def begin(self):
        pass
