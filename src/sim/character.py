import pygame


class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.image.load(f'../art/sim_sprites/{name}.png')
        self.rect = self.image.get_rect()
