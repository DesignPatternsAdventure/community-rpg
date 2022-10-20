import arcade
from rpg.constants import ITEM_MAP
from rpg.sprites.character_sprite import Direction

ITEM_SPRITE_SHEET = ":misc:items.png"
ITEM_SPRITE_SIZE = 16


class ItemSprite(arcade.Sprite):
    def __init__(self, item, player_sprite):
        super().__init__()
        self.textures = arcade.load_textures(
            file_name=ITEM_SPRITE_SHEET,
            image_location_list=self.get_image_locations(),
        )
        self.textures_mirrored = arcade.load_textures(
            file_name=ITEM_SPRITE_SHEET,
            image_location_list=self.get_image_locations(),
            mirrored=True
        )
        self.player_sprite = player_sprite
        self.texture = self.textures[ITEM_MAP[item]]
        self.item = item

    def get_image_locations(self):
        image_locations = []
        for i in range(8):
            for j in range(8):
                image_locations.append([
                    i * ITEM_SPRITE_SIZE,
                    j * ITEM_SPRITE_SIZE,
                    ITEM_SPRITE_SIZE,
                    ITEM_SPRITE_SIZE])
        return image_locations

    def on_update(self, delta_time):
        super().on_update(delta_time)
        direction = self.player_sprite.direction
        self.center_y = self.player_sprite.center_y - 5

        if direction == Direction.LEFT:
            self.center_x = self.player_sprite.center_x - 10
            self.texture = self.textures_mirrored[ITEM_MAP[self.item]]

        if direction == Direction.RIGHT:
            self.center_x = self.player_sprite.center_x + 10
            self.texture = self.textures[ITEM_MAP[self.item]]

        if direction == Direction.UP:
            self.center_x = self.player_sprite.center_x - 15
            self.texture = self.textures_mirrored[ITEM_MAP[self.item]]

        if direction == Direction.DOWN:
            self.center_x = self.player_sprite.center_x + 15
            self.texture = self.textures[ITEM_MAP[self.item]]
