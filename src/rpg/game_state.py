import pickle
from pathlib import Path

import arcade
import json

from .constants import MAP, MAP_SAVE_FILE, PLAYER_SAVE_FILE, SAVE_FILE_DIR


class GameState():
    """
    Class to manage game state.
    """

    def __init__(self):
        Path(SAVE_FILE_DIR).mkdir(exist_ok=True)
        self.map_path = self.get_map_path()
        self.map = self.get_map_data()
        self.player = None

    def get_map_path(self):
        path = Path(MAP_SAVE_FILE)
        if path.is_file():
            return path
        return MAP

    def get_map_data(self):
        path = Path(MAP_SAVE_FILE)
        if path.is_file():
            with open(MAP_SAVE_FILE) as f:
                return json.load(f)
        with open(MAP) as f:
            return json.load(f)

    def get_player_data(self):
        path = Path(PLAYER_SAVE_FILE)
        if path.is_file():
            with open(PLAYER_SAVE_FILE, 'rb') as f:
                return pickle.load(f)
        return None

    def save_map_data(self):
        with open(MAP_SAVE_FILE, 'w') as f:
            json.dump(self.map, f)
        return

    def save_player_data(self):
        if self.player:
            data = {
                'x': self.player.center_x,
                'y': self.player.center_y,
                'inventory': self.compress_inventory()
            }
            with open(PLAYER_SAVE_FILE, 'wb') as f:
                pickle.dump(data, f)
        return

    def remove_sprite_from_map(self, sprite):
        # TODO make this robust
        self.map['layers'][5]['objects'] = []
        self.save_map_data()

    def compress_inventory(self):
        compressed = []
        for item in self.player.inventory:
            tmp = {
                'item': item.properties['item'],
                'count': item.properties['count']
            }
            try:
                tmp.update({
                    'filename': item.filename
                })
            except:
                tmp.update({
                    'texture': item.texture.name,
                    'image': item.texture.image
                })
            if "equippable" in item.properties:
                tmp["equippable"] = True
            compressed.append(tmp)
        return compressed

    def decompress_inventory(self, data):
        decompressed = []
        for item in data['inventory']:
            sprite = None
            if 'filename' in item:
                sprite = arcade.Sprite(filename=item['filename'])
            else:
                texture = arcade.Texture(
                    name=item['texture'], image=item['image'])
                sprite = arcade.Sprite(texture=texture)
            sprite.properties = {
                'item': item['item'],
                'count': item['count']
            }
            if "equippable" in item:
                sprite.properties["equippable"] = True
            decompressed.append(sprite)
        return decompressed
