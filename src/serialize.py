import tilemap
import json

def serialize_tilemap(tiles):
    serialized_tiles = []
    for tile in tiles:
        serialized_tile = {
            'position_x': tile.x,
            'position_y': tile.y,
            'image_path': tile.image_path,        }
        serialized_tiles.append(serialized_tile)
    return json.dumps(serialized_tiles)

def deserialize_tilemap(serialized_data):
    serialized_tiles = json.loads(serialized_data)
    tiles = []
    for serialized_tile in serialized_tiles:
        tile = tilemap.Tile(
            x=serialized_tile['position_x'],
            y=serialized_tile['position_y'],
            image_path=serialized_tile['image_path'],
        )
        tiles.append(tile)
    return tiles
