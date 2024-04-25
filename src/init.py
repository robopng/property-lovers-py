import pygame
# it gets upset without the src. for some of these
from src.sim.sim_showrunner import SimShowrunner
from src.platform.platform_showrunner import PlatformShowrunner
from src.menu.main_menu_showrunner import MainMenuShowrunner
from src.renderer import Renderer

# pygame setup
pygame.init()
# all users of larger monitors get destroyed
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
# the four runners and their universal renderer -
# no handovers or interactions need to be considered within the bounds
# of init.py
renderer = Renderer(screen, clock)
code_table = {
    "SIM": SimShowrunner(renderer),
    "PLAT": PlatformShowrunner(renderer),
    "MAIN_MENU": MainMenuShowrunner(renderer),
    "MENU": MainMenuShowrunner(renderer),  # functionless until the game expands to have a separate in-level menu
    "NONE": None,
    "LAST": None  # memory code
}
code = "PLAT"

# yield complete control to respective showrunner
# when showrunner needs to stop, it will return code of the next showrunner in line
while (condition := code_table[code]) is not None:
    code_table["LAST"] = condition
    code = condition.begin()
    # pass unconditionally. in the case we are in a local menu (e.g. hitting the menu button inside the sim),
    # use memory to return to where we opened the menu from
    if "MENU" in code:
        code_table[code].begin()
        code = "LAST"
pygame.quit()
