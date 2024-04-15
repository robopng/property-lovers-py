import pygame


class Renderer:
    def __init__(self, screen, clock, fps=60):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.background = None
        self.background_rect = None

    def display_background(self, name):
        """
        Display a given background by name.
        :param name: the name of the background to be displayed, without path references
        """
        # NEVER change this. ever. this is tantamount to an absolute path, NOTHING else will work.
        # Believe me.
        # I have tried.
        self.background = pygame.image.load(f"../art/backgrounds/{name}")
        self.background_rect = self.background.get_rect()
        self.screen.blit(self.background, self.background_rect)

    def display_sprites(self, targets):
        """
        Draw a set of sprite groups of predefined sprites, then display everything on the screen
        :param targets: zero or more sprite groups to be displayed; if there are no targets,
                        the method will only flip the screen.
        """
        for target in targets:
            target.update()
            target.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def update_fps(self, fps):
        """
        Set a new target fps for the renderer instance.
        :param fps: new target fps
        """
        self.fps = fps


class Box(pygame.sprite.Sprite):
    """
    A testing class for renderer objects.
    Creates a white dummy box sprite to be displayed.
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
