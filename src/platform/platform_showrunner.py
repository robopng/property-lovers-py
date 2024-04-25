import pygame

from src.platform.level_scanner import LevelScanner
from src.platform.player import Player


class PlatformShowrunner:
    def __init__(self, renderer):
        self.renderer = renderer
        self.level_code = 1
        self.targets = pygame.sprite.Group()
        self.player = None
        self.level = None
        self.level_tile_group = None

        self.resume = False

    def begin(self):
        if not self.resume:
            self.level = LevelScanner(self.level_code)
            self.level.set_player_block()
            self.level.set_block_texture_array()
            self.level_tile_group = self.level.get_block_group()
            self.player = Player(self.level.get_player_pos())
            self.targets.add(self.player)
            self.resume = True
        while True:
            collisions = pygame.sprite.groupcollide(self.targets, self.level_tile_group, False, False, collided=pygame.sprite.collide_mask)
            if self.player in collisions:
                for collision in collisions[self.player]:
                    if collision.get_name() != "BLACK": self.player.collide(collision.get_rect())
            if (direction := self.player.check_bounds(self.renderer.screen)) is not None:
                self.level.move_block(direction)
                self.level.set_block_texture_array()
                self.level_tile_group = self.level.get_block_group()
            # check collision
            #  if player is colliding with another sprite, process consequence
            #  if player is colliding with the floor, keep on floor
            #  if player is colliding with block boundary, move the current block
            #   and reload the new block
            self.poll()
            self.renderer.display((self.level_tile_group, self.targets))
        # if player survived, and EoL reached, write out stats
        # if player died, give option to retry
        self.resume = False
        return "SIM"

    def poll(self):
        # events to consider:
        # window close
        # keyboard presses for movement
        # keyboard presses for hotkeys (e.g. esc for menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            if event.type == pygame.KEYUP:
                self._poll_keyup(event)
            if event.type == pygame.KEYDOWN:
                self._poll_keydown(event)


    def _poll_keyup(self, event):
        key = event.key
        if key == pygame.K_SPACE: self.player.jump()
        if key == pygame.K_d: self.player.halt('right')
        if key == pygame.K_a: self.player.halt('left')

    def _poll_keydown(self, event):
        key = event.key
        if key == pygame.K_d: self.player.moving('right')
        if key == pygame.K_a: self.player.moving('left')
