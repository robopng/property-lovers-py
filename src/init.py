import pygame
from sim.sim_showrunner import SimShowrunner
from platform.platform_showrunner import PlatformShowrunner
from renderer import Renderer

# pygame setup
pygame.init()
# all users of larger monitors get destroyed
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
in_sim = in_plat = False
# in_menu = True

renderer = Renderer()
simulator = SimShowrunner()
platformer = PlatformShowrunner()
main_menu = None
menu = None
code_table = {
    "SIM": simulator,
    "PLAT": platformer,
    "MAIN_MENU": main_menu,
    "MENU": menu,
    "NONE": None
}
code = "MAIN_MENU"

# # poll for events
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         pygame.quit()

# yield complete control to respective showrunner
# when showrunner needs to stop, it will return code of the next showrunner in line
while condition := code_table[code] is not None:
    # see controller.py
    condition.begin(renderer)
    code = condition.get_code()

# # flip() the display to put your work on screen
# pygame.display.flip()
#
# clock.tick(60)  # limits FPS to 60
pygame.quit()
