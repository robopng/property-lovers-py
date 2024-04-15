import pygame


class Renderer:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.background = None

    def display(self, targets):
        for target in targets:
            target.update()
            target.draw(self.screen)
        pygame.display.flip()


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


pygame.init()
rend = Renderer(pygame.display.set_mode((1920, 1080)), pygame.time.Clock())
boxes = pygame.sprite.Group()
running = True
for i in range(10):
    boxes.add(Box(i * 100, i * 100))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    rend.display([boxes])
