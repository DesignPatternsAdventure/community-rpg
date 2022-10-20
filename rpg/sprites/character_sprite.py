"""
Animated sprite for characters that walk around.
"""


import arcade

from enum import Enum
from rpg.constants import SPRITE_SIZE

Direction = Enum("Direction", "DOWN LEFT RIGHT UP")

SPRITE_INFO = {
    Direction.DOWN: [0, 1, 2],
    Direction.LEFT: [3, 4, 5],
    Direction.RIGHT: [6, 7, 8],
    Direction.UP: [9, 10, 11],
}


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.inventory = []
        self.direction = Direction.LEFT

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            if self.change_x > 0:
                self.direction = Direction.RIGHT
            else:
                self.direction = Direction.LEFT
        else:
            if self.change_y > 0:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN

        if self.cur_texture_index not in SPRITE_INFO[self.direction]:
            self.cur_texture_index = SPRITE_INFO[self.direction][0]

        self.texture = self.textures[self.cur_texture_index]
