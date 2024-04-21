import pygame


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, path, content=None):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.content = content

    def transform_image(self, width_and_height):
        self.image = pygame.transform.scale(self.image, width_and_height)
        self.rect = self.image.get_rect()

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def has_content(self):
        return self.content is not None
