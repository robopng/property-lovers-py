class Controller:
    def __init__(self, return_code, state, renderer):
        self.return_code = return_code
        self.state = state
        self.renderer = renderer

    def begin(self):
        """
        Begin the logical process of the Controller.
        """
        # make a window & cast nothing onto it (will be handled by children)

    def get_code(self):
        return self.return_code

    def get_state(self):
        return self.state
