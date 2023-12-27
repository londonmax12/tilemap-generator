import tilemap as tm
import json

def serialize_variation(variation):
    return {
        'x': variation.x,
        'y': variation.y,
        'name': variation.name,
        'rotation': variation.rotation
    }

def serialize_tile(tile):
    serialized_variations = [serialize_variation(variation) for variation in tile.variations]

    serialized_tile = {
        'id': tile.id,
        'position_x': tile.x,
        'position_y': tile.y,
        'name': tile.name, 
        'image_path': tile.image_path,
        'variations': serialized_variations,
        'children': [serialize_tile(child) for child in tile.children]
    }
    return serialized_tile

def deserialize_variation(json_variation):
    return tm.TileVariation(
        x = json_variation['x'],
        y = json_variation['y'],
        name = json_variation['name'],
        rotation = json_variation['rotation']
    )

def deserialize_tile(json_tile):
    tile = tm.Tile(json_tile['image_path'], (json_tile['position_x'], json_tile['position_y']), json_tile['id'], json_tile['name'])
        
    if 'variations' in json_tile:
        tile.variations = [deserialize_variation(variation) for variation in json_tile['variations']]
    
    if 'children' in json_tile:
        tile.children = [deserialize_tile(child) for child in json_tile['children']]
    
    return tile

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

def deserialize_tilemap(serialized_data):
    serialized_data = json.loads(serialized_data)
    tilemap_info = serialized_data.get('tilemap_info', {})
    tilemap = tm.Tilemap(tilemap_info.get('tile_width', 32), tilemap_info.get('tile_height', 32))

    for serialized_tile in serialized_data['tiles']:
        tile = deserialize_tile(serialized_tile)
        tilemap.tiles.append(tile)

    return tilemap