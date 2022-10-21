"""
Constant values for the game
"""
import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Python Community RPG"
TILE_SCALING = 1.0
SPRITE_SIZE = 32

# How fast does the player move
MOVEMENT_SPEED = 10

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# What map, and what position we start at
STARTING_MAP = "main_map_new"
STARTING_X = 110
STARTING_Y = 105

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]
INVENTORY = [arcade.key.I]
SEARCH = [arcade.key.E]

# Message box
MESSAGE_BOX_FONT_SIZE = 18
MESSAGE_BOX_MARGIN = 10

# How fast does the camera pan to the user
CAMERA_SPEED = 0.1

ITEM_MAP = {
  'pickaxe': 43
}
