import pygame
from src.sim.dialog_controller import DialogController
from src.sim.character import CharacterSprite
from src.menu_element import MenuSprite


class SimShowrunner:
    """
    The showrunner for the dating sim aspect of the game.
    SimShowrunner handles the core loop of the dating sim and, using
    a renderer clas passed in construction, also handles the logic for
    when to display its elements.
    """
    def __init__(self, renderer):
        # find a way to change this dynamically later
        # probably will come in from a save state file
        self.date_code = 0
        self.current_date_success = 0
        # sprite and menu box initialization
        self.npc_house = CharacterSprite(f'../art/sim_sprites/house_{self.date_code}.png')
        # self.pc_house
        # self.player
        self.sprites = pygame.sprite.Group()
        # too tired to think of a better method for this right now
        self.NPC_DIALOG = 4
        self.PLAYER_DIALOG = 1
        self.STATICS = 0
        menu_box_path = '../art/sim_sprites/dialogue_box.png'
        self.boxes = (
            # return to menu button
            MenuSprite(200, 200, 100, 100, menu_box_path, content="Menu", consequence=-10),
            # begin
            # MenuSprite(500, 500, 100, 100, consequence=-101)
            # player dialog 1
            MenuSprite(0, 0, 100, 100, menu_box_path, consequence=1),
            # player dialog 2
            MenuSprite(150, 0, 100, 100, menu_box_path, consequence=2),
            # player dialog 3
            MenuSprite(300, 0, 100, 100, menu_box_path, consequence=3),
            # npc dialog
            MenuSprite(200, 500, 100, 100, menu_box_path, consequence=-100),
        )
        self.sprites.add(self.boxes[self.STATICS])
        self.sprites.add(self.npc_house)
        self.renderer = renderer
        self.scroll = DialogController()

    def begin(self):
        """
        Begin the loop of the dating sim.
        When finished, or if interrupted, this method will return a code corresponding
        to the next appropriate flow action in gameplay. See init.py for the list of
        codes and their flow actions.
        """

        # render effects; fade in, show house, sleep slightly for dramatic pause
        # dialog files ALWAYS start from an NPC dialog line;
        # if this method is being returned to from a menu interrupt, the loop has already guaranteed
        # that the scroll was rewound to an npc dialog line.
        if not self.scroll.has_file(): self.scroll.load_file(self.date_code)
        self.boxes[self.NPC_DIALOG].set_content(self.scroll.current_line())  # FROM START in dialog file
        self.sprites.add(self.boxes[self.NPC_DIALOG])
        self.renderer.set_background(f'{self.date_code}_BG')
        self.renderer.display(self.sprites, text=True)
        while self.scroll.has_next():
            # await click on last dialog to proceed
            while (result := self.poll()) is None: pass
            # every time poll is called it needs to handle the static boxes
            # handling the return, at least, cannot be delegated to a function (as far as I'm aware)
            if result[0] == -10: return "MENU"
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
                while (result := self.poll()) is None: pass
                if result[0] == -10:
                    # far easier than changing the pre-loop code to accommodate returns while awaiting
                    # also a better creative choice, in my opinion
                    self.scroll.walk_back()
                    self.sprites.remove(self.boxes[self.PLAYER_DIALOG:self.NPC_DIALOG])
                    self.sprites.add(self.boxes[self.NPC_DIALOG])
                    return "MENU"
                # update relevant text boxes
                self.scroll.jump(result[0])
                self.boxes[self.NPC_DIALOG].set_content(self.scroll.current_line())

            self.sprites.remove(self.boxes[self.PLAYER_DIALOG:self.NPC_DIALOG])
            self.sprites.add(self.boxes[self.NPC_DIALOG])
            self.renderer.display(self.sprites, text=True)
            # sleep
        # fade out effects, show how the player did, sleep
        while (result := self.poll()) is None: pass
        if result[0] == -10: return "MENU"
        # write save state
        self.scroll.empty_file()
        self.date_code += 1
        return "PLAT"

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # certainly, there must be some consequence to having it like this.
                # otherwise, everything would use this instead of the run=True method...
                # still, I can't think of one, so it stays!
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                r = [box.get_consequence()
                     for box in self.boxes
                     if box.get_rect().collidepoint(pygame.mouse.get_pos())
                     and box in self.sprites]
                return r if r != [] else None
        return None
