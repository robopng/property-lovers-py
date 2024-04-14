class Controller:
    def __init__(self, return_code, state):
        self.return_code = return_code
        self.state = state

    def begin(self, renderer):
        """
        Begin the logical process of the Controller.
        :param renderer: A window to render the showrunner's objects onto
        """
        # make a window & cast nothing onto it (will be handled by children)

    def get_code(self):
        return self.return_code

    def get_state(self):
        return self.state
