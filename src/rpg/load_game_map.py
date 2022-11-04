"""
Load maps
"""
import json
from collections import OrderedDict

import arcade
from loguru import logger

from .constants import TILE_SCALING
from .sprites.character_sprite import CharacterSprite
from .sprites.path_following_sprite import PathFollowingSprite
from .sprites.random_walking_sprite import RandomWalkingSprite

GOD_MODE = False


class GameMap:
    name = None
    scene = None
    map_layers = None
    map_size = None
    properties = None
    background_color = arcade.color.AMAZON


def load_map(map=None):
    """
    Load a map
    """

    game_map = GameMap()
    game_map.map_layers = OrderedDict()

    # List of blocking sprites

    layer_options = {
        "trees_blocking": {
            "use_spatial_hash": True,
        },
        "misc_blocking": {
            "use_spatial_hash": True,
        },
        "bridges": {
            "use_spatial_hash": True,
        },
        "water_blocking": {
            "use_spatial_hash": True,
        },
    }

    # Read in the tiled map
    logger.debug(f"Loading map: {map}")
    my_map = arcade.tilemap.load_tilemap(
        map, scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    if "characters" in my_map.object_lists:
        f = open("src/resources/data/characters_dictionary.json")
        character_dictionary = json.load(f)
        character_object_list = my_map.object_lists["characters"]

        for character_object in character_object_list:

            if "type" not in character_object.properties:
                logger.debug(
                    f"No 'type' field for character in map {map}. {character_object.properties}"
                )
                continue

            character_type = character_object.properties["type"]
            if character_type not in character_dictionary:
                logger.debug(
                    f"Unable to find '{character_type}' in characters_dictionary.json."
                )
                continue

            character_data = character_dictionary[character_type]
            shape = character_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if character_object.properties.get("movement") == "random":
                    character_sprite = RandomWalkingSprite(
                        f":characters:{character_data['images']}", game_map.scene
                    )
                else:
                    character_sprite = CharacterSprite(
                        f":characters:{character_data['images']}"
                    )
                character_sprite.position = shape
            elif isinstance(shape, list) and len(shape[0]) == 2:
                # Rect or polygon.
                location = [shape[0][0], shape[0][1]]
                character_sprite = PathFollowingSprite(
                    f":characters:{character_data['images']}"
                )
                character_sprite.position = location
                path = []
                for point in shape:
                    location = [point[0], point[1]]
                    path.append(location)
                character_sprite.path = path
            else:
                logger.debug(
                    f"Unknown shape type for character with shape '{shape}' in map {map}."
                )
                continue

            logger.debug(
                f"Adding character {character_type} at {character_sprite.position}"
            )
            game_map.scene.add_sprite("characters", character_sprite)

    # Get all the tiled sprite lists
    # Get all the tiled sprite lists
    game_map.map_layers = my_map.sprite_lists

    # Define the size of the map, in tiles
    game_map.map_size = my_map.width, my_map.height

    # Set the background color
    game_map.background_color = my_map.background_color

    game_map.properties = my_map.properties

    # Any layer with '_blocking' in it, will be a wall
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "_blocking" in layer and not GOD_MODE:
            try:
                game_map.scene.remove_sprite_list_by_object(sprite_list)
            except:
                logger.debug(f"{layer} has no objects")

            game_map.scene["wall_list"].extend(sprite_list)

    return game_map
