import pygame


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
