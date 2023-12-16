"""
serialize.py

This script contains the logic to serialize a tilemap in a JSON format

Created by Mercury Dev
Created on 2023-12-17
"""

import tilemap as tm
import json

def serialize_tilemap(tilemap):
    serialized_tiles = []
    for tile in tilemap.tiles:
        serialized_tile = {
            'position_x': tile.x,
            'position_y': tile.y,
            'image_path': tile.image_path,        }
        serialized_tiles.append(serialized_tile)
    return json.dumps(serialized_tiles)

def deserialize_tilemap(serialized_data):
    serialized_tiles = json.loads(serialized_data)
    tilemap = tm.Tilemap(32, 32)
    for serialized_tile in serialized_tiles:
        tile = tm.Tile(
            x=serialized_tile['position_x'],
            y=serialized_tile['position_y'],
            image_path=serialized_tile['image_path'],
        )
        tilemap.tiles.append(tile)

    return tilemap
