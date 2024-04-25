import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.image

    def set_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y
