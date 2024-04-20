import pygame
# it gets upset without the src. for some of these
from src.sim.sim_showrunner import SimShowrunner
from src.platform.platform_showrunner import PlatformShowrunner
from src.menu.main_menu_showrunner import MainMenuShowrunner
from src.menu.menu_showrunner import MenuShowrunner
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
simulator = SimShowrunner(renderer)
platformer = PlatformShowrunner(renderer)
main_menu = MainMenuShowrunner(renderer)
menu = MenuShowrunner(renderer)
code_table = {
    "SIM": simulator,
    "PLAT": platformer,
    "MAIN_MENU": main_menu,
    "MENU": menu,
    "NONE": None,
    "LAST": None  # memory code
}
code = "MAIN_MENU"

# yield complete control to respective showrunner
# when showrunner needs to stop, it will return code of the next showrunner in line
while (condition := code_table[code]) is not None:
    code_table["LAST"] = condition
    # see controller.py
    condition.begin()
    # pass unconditionally. in the case we are in a local menu (e.g. hitting the esc key inside the sim),
    # use memory to return to where we opened the menu from
    code = condition.get_code() if code != "MENU" else "LAST"
pygame.quit()
