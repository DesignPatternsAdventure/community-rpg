"""
Load maps
"""
import json
import os
from collections import OrderedDict
from os.path import isfile, join

import arcade

from rpg.sprites.character_sprite import CharacterSprite
from rpg.constants import TILE_SCALING, STARTING_MAP
from rpg.sprites.path_following_sprite import PathFollowingSprite
from rpg.sprites.random_walking_sprite import RandomWalkingSprite

GOD_MODE = False
LOAD_ALL_MAPS = False


class GameMap:
    name = None
    scene = None
    map_layers = None
    map_size = None
    properties = None
    background_color = arcade.color.AMAZON


def load_map(map_name):
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
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(
        map_name, scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    if "characters" in my_map.object_lists:
        f = open("resources/data/characters_dictionary.json")
        character_dictionary = json.load(f)
        character_object_list = my_map.object_lists["characters"]

        for character_object in character_object_list:

            if "type" not in character_object.properties:
                print(
                    f"No 'type' field for character in map {map_name}. {character_object.properties}"
                )
                continue

            character_type = character_object.properties["type"]
            if character_type not in character_dictionary:
                print(
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
                print(
                    f"Unknown shape type for character with shape '{shape}' in map {map_name}."
                )
                continue

            print(f"Adding character {character_type} at {character_sprite.position}")
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
                print(f'{layer} has no objects')

            game_map.scene["wall_list"].extend(sprite_list)

    return game_map


def load_maps():
    """
    Load all the Tiled maps from a directory.
    (Must use the .json extension.)
    """

    # Directory to pull maps from
    map_dir = "resources/maps"

    # Dictionary to hold all our maps
    load_maps.map_list = {}

    if LOAD_ALL_MAPS:
        # Pull names of all json files in that path
        load_maps.map_file_names = [
            f[:-5]
            for f in os.listdir(map_dir)
            if isfile(join(map_dir, f)) and f.endswith(".json")
        ]
        load_maps.map_file_names.sort()
    else:
        # Load starting map only
        load_maps.map_file_names = [STARTING_MAP]

    # Loop and load each file
    load_maps.file_count = len(load_maps.map_file_names)
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"{map_dir}/{map_name}.json")

    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    done = len(load_maps.map_file_names) == 0
    return done, progress, load_maps.map_list


load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
