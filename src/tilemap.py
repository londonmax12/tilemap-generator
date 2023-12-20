"""
tilemap.py

This script contains the tilemap logic

Created by Mercury Dev
Created on 2023-12-16
"""

from PIL import Image
import uuid
import os

class Tile:
    def __init__(self, image_path, position, id = -1) -> None:
        self.name = os.path.splitext(os.path.basename(image_path))[0]
        self.id = str(uuid.uuid4()) if id == -1 else id
        self.x = position[0]
        self.y = position[1]
        self.image_path = image_path
        self.children = []
        self.set_image()
     
    def set_image(self, image_path = ""):
        try:
            self.img = Image.open(self.image_path if image_path == "" else image_path)
        except:
            self.img = None
            
    def add_child(self, child_tile):
        self.children.append(child_tile)

class Tilemap:
    def __init__(self, tile_width, tile_height) -> None:
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = []

    def create_tilemap_img(self):
        max_width = 0
        max_height = 0

        for tile in self.tiles:
            max_width = max(max_width, tile.x + 1)
            max_height = max(max_height, tile.y + 1)

            for child in tile.children:
                max_width = max(max_width, child.x + 1)
                max_height = max(max_height, child.y + 1)

        out_img = Image.new("RGBA", (max_width * self.tile_width, max_height * self.tile_height))

        for tile in self.tiles:
            for child in tile.children:
                child_resized_img = child.img.resize((self.tile_width, self.tile_height), Image.ANTIALIAS)
                out_img.paste(child_resized_img, (self.tile_width * (child.x + tile.x), self.tile_height * (child.y + tile.y)))

            tile_resized_img = tile.img.resize((self.tile_width, self.tile_height), Image.ANTIALIAS)
            out_img.paste(tile_resized_img, (self.tile_width * tile.x, self.tile_height * tile.y))

        return out_img
    
    def get_next_tile_position(self, tile_parent = 0):
        if not tile_parent:
            return (0, len(self.tiles))
        
        return (tile_parent.x + 1, tile_parent.y)
    
    def search_children(self, tile, name):
        for child in tile.children:
            if child.name == name:
                return child
            if len(child.children):
                return self.search_children(child, name)
            return None

    def get_tile_by_name(self, name):
        for tile in self.tiles:
            if tile.name == name:
                return tile
            return self.search_children(tile, name)