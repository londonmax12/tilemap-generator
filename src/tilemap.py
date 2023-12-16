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

def create_tilemap_img(tiles, tile_width, tile_height):
    width = 1
    height = 1

    for tile in tiles:
        if (tile.x + 1 > width):
            width = tile.x + 1
        if (tile.y + 1 > height):
            height = tile.y + 1

    out_img = Image.new("RGBA", (width * tile_width, height * tile_height))

    for tile in tiles:
        out_img.paste(tile.img, (tile_width * tile.x, tile_height * tile.y))

    return out_img