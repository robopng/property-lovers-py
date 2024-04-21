from src.controller import Controller


class PlatformShowrunner:
    def __init__(self, renderer):
        pass

    def begin(self):
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
        return "MAIN_MENU"

    def poll(self):
        # events to consider:
        # window close
        # keyboard presses for movement
        # keyboard presses for hotkeys (e.g. esc for menu)
        pass
