"""
serialize.py

This script contains the logic to serialize a tilemap in a JSON format

Created by Mercury Dev
Created on 2023-12-17
"""

import tilemap as tm
import json

def serialize_tile(tile):
    serialized_tile = {
        'id': tile.id,
        'position_x': tile.x,
        'position_y': tile.y,
        'image_path': tile.image_path,
        'children': [serialize_tile(child) for child in tile.children]
    }
    return serialized_tile

def serialize_tilemap(tilemap):
    serialized_tiles = [serialize_tile(tile) for tile in tilemap.tiles]

    serialized_data = {
        'tilemap_info': {
            'tile_width': tilemap.tile_width,
            'tile_height': tilemap.tile_height,
        },
        'tiles': serialized_tiles,
    }

    return json.dumps(serialized_data)

def deserialize_tile(json_tile):
    tile = tm.Tile(
        image_path=json_tile['image_path'],
        position=(json_tile['position_x'], json_tile['position_y'])
    )

    tile.id = json_tile['id']

    if 'children' in json_tile:
        tile.children = [deserialize_tile(child) for child in json_tile['children']]
    
    return tile

def deserialize_tilemap(serialized_data):
    serialized_data = json.loads(serialized_data)
    tilemap_info = serialized_data.get('tilemap_info', {})
    tilemap = tm.Tilemap(tilemap_info.get('tile_width', 32), tilemap_info.get('tile_height', 32))

    for serialized_tile in serialized_data['tiles']:
        tile = deserialize_tile(serialized_tile)
        tilemap.tiles.append(tile)

    return tilemap