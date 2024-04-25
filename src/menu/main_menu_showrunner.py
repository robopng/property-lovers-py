import pygame

from src.menu_element import MenuSprite


class MainMenuShowrunner:
    def __init__(self, renderer):
        self.renderer = renderer
        menu_box_path = '../art/sim_sprites/dialogue_box.png'
        self.boxes = (
            # quit button
            MenuSprite(
                (renderer.screen.get_width() - 300) / 2, # changed to center, check if it works since I can't run it
                renderer.screen.get_height() / 2 + 50,
                300,
                100,
                menu_box_path,
                content="Quit to Desktop",
                consequence=-1
            ),
            # begin button
            MenuSprite(
                (renderer.screen.get_width() - 300) / 2, # changed to center, check if it works since I can't run it
                renderer.screen.get_height() / 2 - 275,
                300,
                300,
                menu_box_path,
                content="PLAY",
                consequence=1
            ),
            # MenuSprite(150, 0, 100, 100),
            # MenuSprite(300, 0, 100, 100),
            # MenuSprite(200, 500, 100, 100),
        )
        self.sprites = pygame.sprite.Group(self.boxes)

    def begin(self):
        self.renderer.set_background('platformingbg1')
        self.renderer.set_targets(pygame.sprite.Group(self.boxes))
        while True:
            results = self.poll()
            if results is not None and results != []:
                result = results[0]
                if result == -1:
                    exit()
                elif result == 0:
                    return "NONE"
                elif result == 1:
                    return "SIM"
            self.renderer.display(text=True)

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            if event.type == pygame.MOUSEBUTTONUP:
                return [box.get_consequence()
                        for box in self.boxes
                        if box.get_rect().collidepoint(pygame.mouse.get_pos())]
