from PIL import Image

class Tile:
    def __init__(self, x, y, img) -> None:
        self.x = x
        self.y = y
        self.img = img

def create_tilemap_img(tiles, tile_size):
    width = 1
    height = 1

    for tile in tiles:
        if (tile.x + 1 > width):
            width = tile.x + 1
        if (tile.y + 1 > height):
            height = tile.y + 1

    out_img = Image.new("RGBA", (width * tile_size, height * tile_size))

    for tile in tiles:
        out_img.paste(tile.img, (tile_size * tile.x, 0))

    return out_img