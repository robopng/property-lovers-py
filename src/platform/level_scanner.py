import numpy
import pygame.time
from PIL import Image
import numpy as np

import src.renderer
from src.platform.tile_sheet import TileSheet, decide_texture
from src.platform.tile import Tile
from src.static_sprite import StaticSprite


class LevelScanner:
    """
    A class with functionality for processing of platforming level .png layout files.
    When initialized, LevelScanner instances will break down layout files into appropriately
    sized room "blocks" of 30x17 pixels; each pixel in turn represents a 16x16 texture.

    Conversion to texture takes place outside LevelScanner instances, but instances do
    possess functionality for transforming "block" pixel grids into grids of tile types
    based on a pre-determined color coding system.
    """

    COLORS = {
        # "TRANSPARENT": [0, 0, 0, 0],
        "BLACK": [0, 0, 0],
        "WHITE": [255, 255, 255],
        "TILE_TYPE_1": [23, 31, 16],
        "TILE_TYPE_2": [200, 193, 154],
        "TILE_TYPE_3": [79, 73, 39],
        "TILE_TYPE_4": [155, 155, 155],
        "SPIKE_TYPE_1": [0, 204, 255],
        "SPIKE_TYPE_2": [255, 102, 0],
        "SPIKE_TYPE_3": [255, 0, 234],
        "SPIKE_TYPE_4": [0, 255, 191],
        "FIRST_SPAWNPOINT": [255, 250, 141],
        "SPAWNPOINT": [251, 242, 54],
        "ROPE": [138, 11, 48],
        "DETONATOR": [109, 2, 2],
        "TNT": [190, 70, 70],
        "BREAKABLE_DOOR_1": [50, 60, 57],
        "BREAKABLE_DOOR_2": [60, 50, 60],
        "HAMMER": [118, 66, 138],
        "FALLING_BLOCK": [143, 86, 59],
        "LOOSE_BOARD": [102, 57, 49],
    }

    def __init__(self, name):
        self.path_to_level = f'../art/platforming_levels/{name}_layout.png'
        entire_array = np.asarray(Image.open(self.path_to_level).convert('RGB'))
        self.SEGMENT_HEIGHT = 17
        self.SEGMENT_WIDTH = 30
        self.IMAGE_HEIGHT = len(entire_array)
        self.IMAGE_WIDTH = len(entire_array[0])
        # potential alternate method of doing this
        # doesn't seem to preserve the grid aspect of the tiles, though, so row length would need to be defined
        # M = im.shape[0] // 15
        # N = im.shape[1] // 15
        # tiles = [
        #     im[x:x + M, y:y + N]
        #     for x in range(0, im.shape[0], M)
        #     for y in range(0, im.shape[1], N)
        # ]
        # break into rows
        rows = np.vsplit(entire_array,
                         [i * self.SEGMENT_HEIGHT for i in range(self.IMAGE_HEIGHT // self.SEGMENT_HEIGHT)[1:]])
        # get only the rows that contain something of note (non-alpha) ?
        # break rows into squares
        blocks = []
        for row in rows:
            blocks.append(np.hsplit(row,
                                    [i * self.SEGMENT_WIDTH for i in
                                     range(self.IMAGE_WIDTH // self.SEGMENT_WIDTH)[1:]]))
        # functionality of splitter confirmed in the debugger.
        # have a look yourself if you want... the shape should be (17, 30, 4) for most of them
        # ones at the end may come out as slightly larger or smaller depending on issues with filesize
        self.blocks = blocks
        self.current_block = None
        self.sheet = TileSheet("master_sprite_sheet")

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
                        if self.COLORS["FIRST_SPAWNPOINT"] == pixel.tolist():
                            self.current_block = self.blocks[i][j]
                            return

    def set_block_texture_array(self):
        """
        Get a grid of tile textures, tile types, and orientations from the current working block.
        Tile textures are represented by colors, but tile types and orientations by integer values.
        :return: a copy of the current block including tile types and orientations per pixel
        """
        block = self.current_block
        tiled_block = numpy.empty((self.SEGMENT_HEIGHT, self.SEGMENT_WIDTH), dtype=Tile)
        used_tiles = []
        # not entirely sure about the mutability here but really don't want to risk it
        for i in range(len(block)):
            for j in range(len(block[i])):
                # join the tile type to the RGB color for processing outside of method
                # after this each pixel should read [R, G, B, A, TILE, ORIENTATION]
                tileUp = block[i - 1][j] if i > 0 else None
                tileLeft = block[i][j - 1] if j > 0 else None
                tileDown = block[i + 1][j] if i < self.SEGMENT_HEIGHT - 1 else None
                tileRight = block[i][j + 1] if j < self.SEGMENT_WIDTH - 1 else None
                tile_type, orientation = decide_texture(
                    tileUp, tileLeft, tileDown, tileRight, block[i][j]
                )

                # reverse lookup in the dictionary to get the tile's code
                for color in self.COLORS.values():
                    if all(color == block[i][j]):
                        tile_name = list(self.COLORS.keys())[list(self.COLORS.values()).index(color)]

                tile = Tile(self.sheet.get_tile(
                    self.sheet.get_tile_code(tile_name),
                    tile_type,
                    orientation,
                ), tile_name, self.sheet.get_tile_size())

                # not reusing any of the images
                for t in used_tiles:
                    if tile is t:
                        tile = t
                        break

                tiled_block[i][j] = tile
                tile.set_xy(j, i)

        self.current_block = tiled_block

    def get_block_group(self):
        group = pygame.sprite.Group()
        block = self.current_block
        for row in block:
            for tile in row:
                group.add(tile)
        return group

    def get_player_pos(self):
        for i in range(len(self.current_block)):
            for j in range(len(self.current_block[i])):
                if "SPAWNPOINT" in self.current_block[i][j].get_name():
                    return j * self.sheet.get_tile_size(), i * self.sheet.get_tile_size(),

    def move_block(self, direction):
        """
        Given a direction, move the current working block in that direction.
        No handling is provided for movement outside the grid, or into an invalid block.
        :param direction: the direction to move; either "up", "left", "down", or "right
        """
        # just looks better than a bunch of if statements
        i, j = np.argwhere(self.blocks == self.current_block)[0]
        dirs = {
            "up": (i - 1, j),
            "down": (i + 1, j),
            "left": (i, j - 1),
            "right": (i, j + 1)
        }
        i, j = dirs[direction]
        self.current_block = self.blocks[i][j]
