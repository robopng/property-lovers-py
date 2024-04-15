import pygame
from src.controller import Controller
from dialog_scroll import DialogController


class SimShowrunner(Controller):
    def __init__(self, renderer):
        super().__init__("NONE", "NONE", renderer)
        # find a way to change this dynamically later
        # probably will come in from a save state file
        self.date_code = 0
        self.current_date_success = 0
        self.house = f'art/{self.date_code}.png'
        self.scroll = DialogController(f'dialog/{self.date_code}.json')
        self.boxes = pygame.sprite.Group()

    def begin(self):
        # render effects; fade in, show house, sleep slightly for dramatic pause
        # add self.scroll.current_line() to be rendered
        # await event for reading time
        while self.scroll.has_next():
            # check events for if buttons clicked
            next_line = self.scroll.next()
            if len(next_line) == 1: pass  # add the value in next to the renderer
            else:
                # add the three values in next to the renderer
                # render and sleep
                # take inputs until one of them is a click on a box
                # process any other button clicks otherwise
                result = None
                self.scroll.jump(result)
                pass
            # render and sleep
        # fade out effects, show how the player did, sleep
        # await input
        # write save state
        self.return_code = 'PLAT'
