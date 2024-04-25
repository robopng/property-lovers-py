import pygame

from src.platform.level_scanner import LevelScanner


class PlatformShowrunner:
    def __init__(self, renderer):
        self.renderer = renderer
        self.level_code = 1

    def begin(self):
        level = LevelScanner(self.level_code)
        level.set_player_block()
        level.set_block_texture_array()
        while True:
            self.poll()
            self.renderer.display(level.get_block_group())
        # load in level scanner
        # set current platforming block to player's block
        # loop:
        #    check collision
        #     if player is colliding with another sprite, process consequence
        #     if player is colliding with the floor, keep on floor
        #     if player is colliding with block boundary, move the current block
        #      and reload the new block
        #    check input
        #    display
        # if player survived, and EoL reached, write out stats
        # if player died, give option to retry
        return "SIM"

    def poll(self):
        # events to consider:
        # window close
        # keyboard presses for movement
        # keyboard presses for hotkeys (e.g. esc for menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
