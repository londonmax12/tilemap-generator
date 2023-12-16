"""
tilemap.py

This script contains the tilemap logic

Created by Mercury Dev
Created on 2023-12-16
"""

from PIL import Image
import os

class Tile:
    def __init__(self, x, y, image_path) -> None:
        self.x = x
        self.y = y
        self.image_path = image_path
        base = os.path.basename(image_path)
        name = os.path.splitext(base)[0]
        self.name = name
        self.img = Image.open(image_path)

class Tilemap:
    def __init__(self, tile_width, tile_height) -> None:
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = []

    def create_tilemap_img(self):
        width = 1
        height = 1

        for tile in self.tiles:
            if (tile.x + 1 > width):
                width = tile.x + 1
            if (tile.y + 1 > height):
                height = tile.y + 1

        out_img = Image.new("RGBA", (width * self.tile_width, height * self.tile_height))

        for tile in self.tiles:
            resized_img = tile.img.resize((self.tile_width, self.tile_height), Image.ANTIALIAS)
            out_img.paste(resized_img, (self.tile_width* tile.x, self.tile_height * tile.y))

        return out_img