import pygame
import random


def decide_texture(tileUp, tileLeft, tileDown, tileRight, activeTile):
    """
        find neighboring tiles, only 4 around it (if edge tile, assume air on other side of edge)

        4 tile types:
            1. square
            2. end
            3. angle
            4. straight
        orientations: 4 states so 1, 2, 3, 4
            orientations go COUNTER-CLOCKWISE starting from top: up = 1, left = 2, down = 3, right = 4
            square: has none
            end: side that CONNECTS WITH OTHER TILES is the orientation
            angle: orientation has open edge toward requested orientation,
                    as well as open edge to the orientation number % 4 + 1
            straight: open edge is orientation, starting vertical
                    - vertical, randomize 1 or 3 (varies up texture a bit)
                    - horizontal, randomize 2 or 4



        if:
        4 same neighbors:
             straight, face horizontal
        3 same neighbors:
             straight, orient same as 2/3 neighbors
        2 same neighbors:
            if non-same neighbors don't have same x or y location (kiddy corner):
                angle, orient away from 2 non-same neighbors
            else:
                straight, orient same as same neighbors
        1 same neighbor:
            end, orient toward same neighbor
        0 same neighbors:
            square
    """
    orientation = 0
    tile = 0
    same = [activeTile == tileUp, activeTile == tileLeft, activeTile == tileDown, activeTile == tileRight]
    sameSum = same[0] + same[1] + same[2] + same[3]
    if sameSum == 4:
        tile = 3
        orientation = random.choice([2, 4])
    elif sameSum == 3:
        tile = 1
        for x in range(len(same)):
            if not same[x]:
                orientation = (x + 2) % 4 + 1
    elif sameSum == 2:
        if same[0] != same[2]:  # check if we should use angle
            tile = 2
            for x in range(len(same)):
                if not same[x] and not same[(x + 1) % 4]:
                    orientation = x + 1
        else:  # all angled options are gone, same[1] here indicates vert or hoz
            tile = 3
            orientation = random.choice([1 + same[0], 3 + same[0]])
            # options are 1 and 3 (horizontal) if the top is different from middle, 2 and 4 otherwise
    elif sameSum == 1:
        tile = 3
        for x in range(len(same)):
            if same[x]:
                orientation = (x + 2) % 4
    else:
        tile = 0
        orientation = random.randint(1, 4)  # random orientation for solo tile
    return tile, orientation


class Tile(pygame.sprite.Sprite):
    TILES = {
        "TILE_TYPE_1": 0,
        "TILE_TYPE_2": 1,
        "SPIKE_TYPE_1": 2,
        "SPIKE_TYPE_2": 3,
    }
    TILE_WIDTH = 16
    TILE_HEIGHT = 16
    COLORKEY = (0, 0, 0)

    def __init__(self, name):
        super().__init__()
        self.sheet = pygame.image.load(f'../art/platforming_sprites/{name}.png')

    def get_tile_code(self, tile_type):
        return self.TILES[tile_type]

    def get_tile(self, tile_code, tile, orientation):
        image = pygame.transform.rotate(
            self._image_at(
                (
                    tile * self.TILE_WIDTH,  # x
                    tile_code * self.TILE_HEIGHT,  # y
                    self.TILE_WIDTH,  # width
                    self.TILE_HEIGHT  # height
                )
            ),
            orientation * 90  # never do any other degree turn here or rescaling will be required
        )
        return image, image.get_rect()

    def _image_at(self, rectangle):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.COLORKEY, pygame.RLEACCEL)
        return image
