import pygame
from src.controller import Controller
from dialog_scroll import DialogController


class SimShowrunner(Controller):
    """
    The showrunner for the dating sim aspect of the game.
    SimShowrunner handles the core loop of the dating sim and, using
    a renderer clas passed in construction, also handles the logic for
    when to display its elements.
    """
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
        """
        Begin the loop of the dating sim.
        When finished, or if interrupted, the object's return_code variable will be
        updated to match either the next segment of the game or a return to the menu,
        respectively.
        Codes: {
                "PLAT" = platform_showrunner
                "MAIN_MENU" = main_menu_showrunner
                "MENU" = menu_showrunner
                "NONE" = terminate
                "SIM" = this
                "LAST" = memory code (irrelevant)
               }
        """
        running = True
        # render effects; fade in, show house, sleep slightly for dramatic pause
        # add self.scroll.current_line() to be rendered
        # await event for reading time
        while self.scroll.has_next() and running:
            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                # if event.type == mouse click: pass to listeners
                # if event.type == something else: do something else

            next_line = self.scroll.next()
            if len(next_line) == 1: pass  # add the value in next to the renderer
            else:
                # add the three values in next to the renderer
                # render and sleep
                # take inputs until one of them is a click on a box
                # process any other button clicks otherwise
                result = None
                self.scroll.jump(result)  # and add the value to the renderer
            # render and sleep
        # fade out effects, show how the player did, sleep
        # await input
        # write save state
        self.return_code = 'PLAT'


class MenuBox(pygame.sprite.Sprite):
    """
    Any menu box item in the dating sim - dialog boxes, menu boxes, etc.
    MenuBox instances may include a listener, or may be static elements on the screen.
    """
    def __init__(self, x, y, length, width):
        pygame.sprite.Sprite.__init__()
        # when we get images for the menu elements use those
        # self.image = pygame.image.load("path/to/element")
        self.image = pygame.Surface(length, width)
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.listener = None

    def set_listener(self, listener):
        """
        Add a listener to the MenuBox instance for instances that are subject to player interaction.
        :param listener: listener to be added to the box object
        """
        pass

    def check_listener(self, event):
        """
        Check whether an event that has occurred is within the bounds of this MenuBox instance.
        :param event: the event triggered
        :return: whether the provided event pertains to this listener
        """
        pass
