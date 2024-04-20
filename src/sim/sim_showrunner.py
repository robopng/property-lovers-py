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
        self.npc_house = CharacterSprite(f'../art/sim_sprites/{self.date_code}.png')
        # self.pc_house
        # self.player
        # always display static boxes
        self.sprites = pygame.sprite.Group()
        self.boxes = (
            # return to menu button
            MenuSprite(200, 200, 100, 100, content="Menu", consequence=-10),
            # begin
            # MenuSprite(500, 500, 100, 100, consequence=-101)
            # player dialog 1
            MenuSprite(0, 0, 100, 100, consequence=1),
            # player dialog 2
            MenuSprite(150, 0, 100, 100, consequence=2),
            # player dialog 3
            MenuSprite(300, 0, 100, 100, consequence=3),
            # npc dialog
            MenuSprite(200, 500, 100, 100, consequence=-100),
        )
        # too tired to think of a better method for this right now
        self.NPC_DIALOG = 4
        self.PLAYER_DIALOG = 1
        self.STATICS = 0
        self.sprites.add(self.boxes[self.STATICS])
        self.renderer = renderer
        self.renderer.set_background(self.date_code)
        self.scroll = DialogController(f'../dialog/{self.date_code}.json')
        # self.running = True

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
        self.boxes[self.NPC_DIALOG].set_content(self.scroll.current_line())  # FROM START in dialog file
        # sit in place until the user gives a valid input
        # self.renderer.display_background()
        # while self.poll(self.static_boxes) is None: pass
        self.sprites.add(self.boxes[self.NPC_DIALOG])
        self.renderer.display(self.sprites, text=True)
        while self.scroll.has_next():
            # await click on last dialog to proceed
            while (result := self.poll(self.boxes)) is None: pass
            # code repetition with player choice handling
            if result[0] == -10:
                self.return_code = 'MENU'
                return self.return_code
            next_line = self.scroll.next()  # FROM LAST in dialog file

            if len(next_line) == 1:
                # no player input needed
                self.boxes[self.NPC_DIALOG].set_content(next_line[0])
            else:
                # add the three values in next to the dynamic boxes
                for box, line in zip(self.boxes[self.PLAYER_DIALOG:self.NPC_DIALOG], next_line):
                    box.set_content(line)

                self.sprites.remove(self.boxes[self.NPC_DIALOG])
                self.sprites.add(self.boxes[self.PLAYER_DIALOG:self.NPC_DIALOG])
                self.renderer.display(self.sprites, text=True)

                # take inputs until one of them is a click on a box
                while (result := self.poll(self.boxes)) is None: pass
                if result[0] == -10:
                    self.return_code = 'MENU'
                    return self.return_code
                # update relevant text boxes
                self.scroll.jump(result[0])
                self.boxes[self.NPC_DIALOG].set_content(self.scroll.current_line())

            self.sprites.remove(self.boxes[self.PLAYER_DIALOG:self.NPC_DIALOG])
            self.sprites.add(self.boxes[self.NPC_DIALOG])
            self.renderer.display(self.sprites, text=True)
            # sleep
        # fade out effects, show how the player did, sleep
        while self.poll(self.boxes) is None: pass
        # write save state
        self.return_code = 'PLAT'
        return self.return_code

    @staticmethod
    def poll(boxes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # certainly, there must be some consequence to having it like this.
                # otherwise, everything would use this instead of the run=True method...
                # still, I can't think of one, so it stays!
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                r = [box.get_consequence() for box in boxes if box.get_rect().collidepoint(pygame.mouse.get_pos())]
                return r if r != [] else None
        return None


class MenuSprite(pygame.sprite.Sprite):
    """
    Any menu box item in the dating sim - dialog boxes, menu boxes, etc.
    MenuBox instances may include a listener, or may be static elements on the screen.
    """
    def __init__(self, x, y, length, width, consequence=0, content=None, visible=True, image='default'):
        super().__init__()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_color = (0, 0, 0)
        self.text_antialias = True
        # self.image = pygame.image.load("path/to/element")
        self.image = pygame.Surface((length, width))
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.content = self.font.render(content, self.text_antialias, self.text_color)
        self.consequence = consequence

    def get_rect(self):
        return self.rect

    def get_content(self):
        return self.content

    def get_content_pos(self):
        return self.rect.x, self.rect.y

    def get_consequence(self):
        return self.consequence

    def set_content(self, content):
        self.content = self.font.render(content, False, (0, 0, 0))

    def has_content(self):
        return self.content is not None


class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
