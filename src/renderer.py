import pygame


class Renderer:
    def __init__(self, screen, clock, background='0', fps=60, targets=pygame.sprite.Group()):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.background = pygame.image.load(f'../art/backgrounds/{background}.png').convert()
        self.background_rect = self.background.get_rect()
        self.targets = targets

    def display(self, targets=None, text=False):
        """
        Display all elements currently contained in the Renderer instance or display
        a given set of targets over the Renderer instance's background
        :param text: whether any of the targets have a textual element
        :param targets: an optional set of new sprite groups to be displayed
        """
        # wouldn't let me use self.targets as a default
        if targets is None: targets = self.targets

        self.screen.blit(self.background, self.background_rect)

        if type(targets) is list or type(targets) is tuple:
            targets = pygame.sprite.Group(targets)
        targets.update()
        targets.draw(self.screen)

        if text:
            self.display_text(targets)

        pygame.display.flip()
        self.clock.tick(self.fps)

    def display_text(self, targets):
        for target in targets:
            if target.has_content():
                self.screen.blit(target.get_content(), target.get_content_pos())
        pygame.display.flip()

    def display_background(self, background=None):
        if background is None: background = self.background
        self.screen.blit(background, background.get_rect())
        pygame.display.flip()

    def set_targets(self, targets):
        self.targets = targets

    def set_background(self, background):
        self.background = pygame.image.load(f'../art/backgrounds/{background}.png').convert()
        self.background_rect = self.background.get_rect()

    def set_fps(self, fps):
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
