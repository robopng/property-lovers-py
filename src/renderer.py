import pygame


class Renderer:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.background = None
        self.background_rect = None

    def display_sprites(self, targets):
        for target in targets:
            target.update()
            target.draw(self.screen)
        pygame.display.flip()

    def display_background(self, name):
        # NEVER change this. ever. this is tantamount to an absolute path, NOTHING else will work.
        # Believe me.
        # I have tried.
        self.background = pygame.image.load(f"../art/backgrounds/{name}")
        self.background_rect = self.background.get_rect()
        self.screen.blit(self.background, self.background_rect)


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
