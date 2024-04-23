from PIL import Image
import numpy as np
from src.platform.decide_texture import decide_texture

COLORS = {
    "TRANSPARENT": [0, 0, 0, 0],
    "BLACK": [0, 0, 0],
    "WHITE": [255, 255, 255],
    "ROPE": [138, 111, 48],
    "TILE_TYPE_1": [23, 31, 16],
    "TILE_TYPE_2": [200, 193, 154],
    "SPIKE_TYPE_1": [0, 204, 255],
    "SPIKE_TYPE_2": [255, 102, 0],
    "SPAWNPOINT": [251, 242, 54],
    "DETONATOR": [109, 2, 2],
    "TNT": [190, 70, 70],
    "BREAKABLE_DOOR": [50, 60, 57],
    "HAMMER": [118, 66, 138],  # collectibles
    "FALLING_BLOCK": [143, 86, 59],
    "LOOSE_BOARD": [102, 57, 49]
}


class LevelScanner:
    """
    A class with functionality for processing of platforming level .png layout files.
    When initialized, LevelScanner instances will break down layout files into appropriately
    sized room "blocks" of 30x17 pixels; each pixel in turn represents a 16x16 texture.

    Conversion to texture takes place outside LevelScanner instances, but instances do
    possess functionality for transforming "block" pixel grids into grids of tile types
    based on a pre-determined color coding system.
    """
    def __init__(self, name):
        # not working with test.png on robo's machine
        self.path_to_level = f'..\\art\\platforming_levels\\{name}.png'
        entire_array = np.asarray(Image.open(self.path_to_level).convert('RGB'))
        self.SEGMENT_HEIGHT = 17
        self.SEGMENT_WIDTH = 30
        self.IMAGE_HEIGHT = len(entire_array)
        self.IMAGE_WIDTH = len(entire_array[0])
        # break into rows
        rows = np.vsplit(entire_array,
                         [i*self.SEGMENT_HEIGHT for i in range(self.IMAGE_HEIGHT//self.SEGMENT_HEIGHT)[1:]])
        # get only the rows that contain something of note (non-alpha) ?
        # break rows into squares
        blocks = []
        for row in rows:
            blocks.append(np.hsplit(row,
                                    [i*self.SEGMENT_WIDTH for i in range(self.IMAGE_WIDTH//self.SEGMENT_WIDTH)[1:]]))
        # functionality of splitter confirmed in the debugger.
        # have a look yourself if you want... the shape should be (17, 30, 4) for most of them
        # ones at the end may come out as slightly larger or smaller depending on issues with filesize
        self.blocks = blocks
        self.current_block = None

    def set_player_block(self):
        """
        Find which block the player spawns in inside the level.
        Once that block is found, make it the current block for future use.
        """
        # 4 for loops. wow! can this be shortened to a np expression..?
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                for row in self.blocks[i][j]:
                    for pixel in row:
                        if pixel.tolist() == COLORS["SPAWNPOINT"]:
                            self.current_block = (i, j)
                            return

    def get_block_texture_array(self):
        """
        Get a grid of tile textures, tile types, and orientations from the current working block.
        Tile textures are represented by colors, but tile types and orientations by integer values.
        :return: a copy of the current block including tile types and orientations per pixel
        """
        block = self.blocks[self.current_block[0], self.current_block[1]]
        # not entirely sure about the mutability here but really don't want to risk it
        for i in range(len(block)):
            for j in range(len(block[i])):
                # join the tile type to the RGB color for processing outside of method
                block[i][j].append(
                    decide_texture(
                        block[i-1][j],  # up
                        block[i][j-1],  # left
                        block[i+1][j],  # down
                        block[i][j+1],  # right
                        block[i][j]     # current
                    )
                )
        return block

    def move_block(self, direction):
        """
        Given a direction, move the current working block in that direction.
        No handling is provided for movement outside the grid, or into an invalid block.
        :param direction: the direction to move; either "up", "left", "down", or "right
        """
        # just looks better than a bunch of if statements
        i, j = self.current_block
        dirs = {
            "up": (i-1, j),
            "down": (i+1, j),
            "left": (i, j-1),
            "right": (i, j+1)
        }
        self.current_block = dirs[direction]
