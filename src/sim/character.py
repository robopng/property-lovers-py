import pygame

import src.static_sprite


class CharacterSprite(src.static_sprite.StaticSprite):
    def __init__(self, path):
        super().__init__(path)

    def set_image(self, path):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
