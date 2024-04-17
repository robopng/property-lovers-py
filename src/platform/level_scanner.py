from PIL import Image
import numpy as np

"""
Scan through a level file image and convert the raw pixel data into
collider objects for use in interaction with the player sprite.
Each collider object is itself a sprite:  
  - Colliders are only created for pixels that border a different color
  - Image determined by solid color of the pixel
  - Collision rules determined by solid color of the pixel
  
  GRAY:
    - Generic wall
    - Halt movement
  YELLOW:
    - One-way wall or platform
    - Only platform for now
    - Allow movement through one way (up)
    - Deny movement in the opposite direction
  LIGHT BROWN:
    - Rope
    - Allow for movement up or down but not side-side
    - Require an event to detach
  DARK BROWN:
    - Falling platform
    - Disappear a set amount of time after collision
  RED:
    - Spike
    - Kill player on collision
  PURPLE:
    - Collectible
    - Disappear after collection
    - Set flag specific collectible obtained for score determination
  WHITE:
    - End of level
    - Begin cleanup process for platforming segment when collided with
"""


class LevelScanner:
    def __init__(self, name):
        # image will be comprised of 30 wide x 17 tall grids arranged 16 wide x 15 tall
        self.path_to_level = f'../art/PlatformingLevels/{name}'
        entire_array = np.asarray(Image.open(self.path_to_level).convert('RGB'))

