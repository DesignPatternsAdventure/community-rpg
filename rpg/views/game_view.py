"""
Main game view
"""

import json
import math

import arcade
import arcade.gui
import rpg.constants as constants
from pyglet.math import Vec2
from rpg.message_box import MessageBox
from rpg.sprites.player_sprite import PlayerSprite


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, map):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Player sprite
        self.player_sprite = None
        self.player_sprite_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map = map

        self.message_box = None

        # Selected Items Hotbar
        self.hotbar_sprite_list = None
        self.selected_item = None

        f = open("resources/data/item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open("resources/data/characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        self.noclip_status = False
        self.animate = False

    def setup_physics(self):
        if self.noclip_status:
            # make an empty spritelist so the character does not collide with anyting
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, arcade.SpriteList()
            )
        else:
            # use the walls as normal
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, self.map.scene["wall_list"]
            )

    def setup(self):
        """Set up the game variables. Call to re-start the game."""

        if self.map.background_color:
            arcade.set_background_color(self.map.background_color)

        map_height = self.map.map_size[1]

        # Spawn the player
        self.player_sprite = PlayerSprite(":characters:Female/Female 22-1.png")
        self.player_sprite.center_x = (
            constants.STARTING_X * constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        )
        self.player_sprite.center_y = (
            map_height - constants.STARTING_Y
        ) * constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        # Set up the hotbar
        self.load_hotbar_sprites()

        self.setup_physics()

    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name="resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def noclip(self, *args, status: bool):
        self.noclip_status = status

        self.setup_physics()

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = 40
        hotbar_height = 80
        sprite_height = 16

        field_width = self.window.width / (capacity + 1)

        x = self.window.width / 2
        y = vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.window.width, hotbar_height, arcade.color.ALMOND
        )
        for i in range(capacity):
            y = vertical_hotbar_location
            x = i * field_width + 5
            if self.selected_item and i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x - 6, x + field_width - 15, y + 25, y - 10, arcade.color.BLACK, 2
                )

            if len(self.player_sprite.inventory) > i:
                item_name = self.player_sprite.inventory[i].properties['item']
            else:
                item_name = ""

            hotkey_sprite = self.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + sprite_height / 2, y + sprite_height / 2, 2.0)
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"     {item_name}"
            arcade.draw_text(text, x, y, arcade.color.ALLOY_ORANGE, 16)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Use the scrolling camera for sprites
        self.camera_sprites.use()

        # Grab each tile layer from the map
        map_layers = self.map.map_layers

        # Draw scene
        self.map.scene.draw()

        # Draw the player
        self.player_sprite_list.draw()

        if self.player_sprite.item:
            self.player_sprite.item.draw()

        for item in map_layers.get("searchable", []):
            arcade.Sprite(
                filename=":misc:shiny-stars.png",
                center_x=item.center_x,
                center_y=item.center_y,
                scale=0.8,
            ).draw()

        # Use the non-scrolled GUI camera
        self.camera_gui.use()

        # Draw the inventory
        self.draw_inventory()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()

        # draw GUI
        self.ui_manager.draw()

    def scroll_to_player(self, speed=constants.CAMERA_SPEED):
        """Manage Scrolling"""

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_show_view(self):
        # Set background color
        if self.map.background_color:
            arcade.set_background_color(self.map.background_color)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        MOVING_UP = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_DOWN = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_RIGHT = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_LEFT = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_UP_LEFT = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        MOVING_DOWN_LEFT = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        MOVING_UP_RIGHT = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        MOVING_DOWN_RIGHT = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )

        if MOVING_UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED

        if MOVING_DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED

        if MOVING_LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED

        if MOVING_RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

        if MOVING_UP_LEFT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_UP_RIGHT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_LEFT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_RIGHT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.on_update(delta_time)

        if self.animate and self.player_sprite.item:
            self.animate_player_item()

        # Update the characters
        try:
            self.map.scene["characters"].on_update(delta_time)
        except KeyError:
            # no characters on map
            pass

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return

        self.selected_item = None

        if key in constants.KEY_UP:
            self.up_pressed = True
        elif key in constants.KEY_DOWN:
            self.down_pressed = True
        elif key in constants.KEY_LEFT:
            self.left_pressed = True
        elif key in constants.KEY_RIGHT:
            self.right_pressed = True
        elif key in constants.INVENTORY:
            self.window.show_view(self.window.views["inventory"])
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
        elif key in constants.SEARCH:
            self.search()
        elif key == arcade.key.KEY_1:
            self.selected_item = 1
            # Will add this to the other keys once there are more items
            self.player_sprite.equip(0)
        elif key == arcade.key.KEY_2:
            self.selected_item = 2
        elif key == arcade.key.KEY_3:
            self.selected_item = 3
        elif key == arcade.key.KEY_4:
            self.selected_item = 4
        elif key == arcade.key.KEY_5:
            self.selected_item = 5
        elif key == arcade.key.KEY_6:
            self.selected_item = 6
        elif key == arcade.key.KEY_7:
            self.selected_item = 7
        elif key == arcade.key.KEY_8:
            self.selected_item = 8
        elif key == arcade.key.KEY_9:
            self.selected_item = 9
        elif key == arcade.key.KEY_0:
            self.selected_item = 10

    def close_message_box(self):
        self.message_box = None

    def search(self):
        """Search for things"""
        map_layers = self.map.map_layers
        if "searchable" not in map_layers:
            self.message_box = MessageBox(
                self, "No searchable items nearby"
            )
            return

        searchable_sprites = map_layers["searchable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.")
        for sprite in sprites_in_range:

            if "item" in sprite.properties:
                self.player_sprite.inventory.append(sprite)
                self.message_box = MessageBox(
                    self,
                    f"{sprite.properties['item']} added to inventory!",
                    f"Press {str(len(self.player_sprite.inventory))} to equip item. Press any key to close this message."
                )
                sprite.remove_from_sprite_lists()
            else:
                print(
                    "The 'item' property was not set for the sprite. Can't get any items from this."
                )

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key in constants.KEY_UP:
            self.up_pressed = False
        elif key in constants.KEY_DOWN:
            self.down_pressed = False
        elif key in constants.KEY_LEFT:
            self.left_pressed = False
        elif key in constants.KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        if self.message_box:
            self.close_message_box()
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y
        if button == arcade.MOUSE_BUTTON_LEFT and self.player_sprite.item:
            closest = arcade.get_closest_sprite(
                self.player_sprite, self.map.map_layers["interactables_blocking"])
            if closest:
              (sprite, dist) = closest
              if dist < constants.SPRITE_SIZE * 2:
                  self.player_sprite.item_target = sprite
                  self.animate = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        pass

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)

    def animate_player_item(self):
        config = self.item_dictionary[self.player_sprite.item.properties['item']]['animation']
        self.animate = self.player_sprite.animate_item(config)
