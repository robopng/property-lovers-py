import pygame
from src.controller import Controller
from src.sim.dialog_scroll import DialogController


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
        # sprite and menu box initialization
        self.sprites = pygame.sprite.Group()
        self.npc_house = CharacterSprite(f'art/sim_sprites/{self.date_code}.png')
        # self.pc_house
        # self.player
        # always display static boxes
        self.static_boxes = (
            # return to menu button
            MenuSprite(0, 0, 100, 100),
            # main dialog display
            MenuSprite(0, 0, 100, 100),
        )
        # only display dynamic boxes when needed
        self.dynamic_boxes = (
            # player dialog 1
            MenuSprite(0, 0, 100, 100),
            # player dialog 2
            MenuSprite(0, 0, 100, 100),
            # player dialog 3
            MenuSprite(0, 0, 100, 100),
        )
        self.renderer = renderer
        self.renderer.set_background(self.date_code)
        self.renderer.set_targets(self.sprites)
        self.scroll = DialogController(f'../dialog/{self.date_code}.json')
        self.running = True

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
        # render effects; fade in, show house, sleep slightly for dramatic pause
        # add self.scroll.current_line() to be rendered
        # sit in place until the user gives a valid input
        while self.poll(self.static_boxes) is None: pass
        while self.scroll.has_next() and self.running:
            # await click on last dialog to proceed
            while self.poll(self.static_boxes) is None: pass
            next_line = self.scroll.next()
            if len(next_line) == 1:
                # no player input needed
                # add the value in next to a static box
                pass
            else:
                # add the three values in next to the dynamic boxes
                # render and sleep
                # take inputs until one of them is a click on a box
                # process any other button clicks otherwise
                result = 0
                self.scroll.jump(result)  # and add the value to the renderer
            # render and sleep
            self.renderer.display()
        # fade out effects, show how the player did, sleep
        while self.poll(self.static_boxes) is None: pass
        # write save state
        self.return_code = 'PLAT'
        return self.return_code

    def poll(self, boxes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return -1
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_boxes = [box for box in boxes if box.get_rect().collidepoint(pygame.mouse.get_pos)]
                for box in clicked_boxes:
                    # try to avoid chaining any more if statements here if possible. maybe consider
                    # a dictionary of consequences
                    # check if the box has player input; return the corresponding code
                    # check if the box is a menu button; process that consequence
                    pass
        return None


class MenuSprite(pygame.sprite.Sprite):
    """
    Any menu box item in the dating sim - dialog boxes, menu boxes, etc.
    MenuBox instances may include a listener, or may be static elements on the screen.
    """
    def __init__(self, x, y, length, width, content=None, visible=True):
        super().__init__()
        # when we get images for the menu elements use those
        # self.image = pygame.image.load("path/to/element")
        self.image = pygame.Surface(length, width)
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.content = content

    def get_rect(self):
        return self.rect

    def set_content(self, content):
        self.content = content

    def has_content(self):
        return self.content is not None


class CharacterSprite(pygame.sprite.Sprite()):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
