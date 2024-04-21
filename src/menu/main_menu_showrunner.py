import pygame

from src.menu_element import MenuSprite


class MainMenuShowrunner:
    def __init__(self, renderer):
        self.renderer = renderer
        self.boxes = (
            # quit
            MenuSprite(200, 200, 100, 100, content="Quit to Desktop", consequence=-1),
            # begin
            MenuSprite(0, 0, 100, 100, content="Play", consequence=1),
            # MenuSprite(150, 0, 100, 100),
            # MenuSprite(300, 0, 100, 100),
            # MenuSprite(200, 500, 100, 100),
        )
        self.sprites = pygame.sprite.Group(self.boxes)
        self.renderer.set_background('BeachBG')
        self.renderer.set_targets(pygame.sprite.Group(self.boxes))

    def begin(self):
        while True:
            results = self.poll()
            if results is not None and results != []:
                result = results[0]
                if result == -1: exit()
                elif result == 0: return "NONE"
                elif result == 1: return "SIM"
            self.renderer.display(text=True)

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                return [box.get_consequence()
                        for box in self.boxes
                        if box.get_rect().collidepoint(pygame.mouse.get_pos())]
