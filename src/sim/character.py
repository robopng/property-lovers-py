import pygame

import src.static_sprite


class CharacterSprite(src.static_sprite.StaticSprite):
    def __init__(self, path, x, y, width, height):
        super().__init__(path)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.transform_image((width, height))
        self.rect.x = x
        self.rect.y = y


    def set_image(self, path):
        self.image = pygame.image.load(path)



