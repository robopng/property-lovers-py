import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, name, size):
        super().__init__()
        self.TILE_SIZE = size
        self.image = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.name = name

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def get_name(self):
        return self.name

    def set_xy(self, x, y):
        self.rect.x = x * self.TILE_SIZE
        self.rect.y = y * self.TILE_SIZE
