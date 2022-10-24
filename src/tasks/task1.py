import arcade

# IMPORTANT: Make sure to play the game first before doing this exercise!
# The game will prompt you to come to this task :)

##############################################################################

# Task 1

# Learning Objective: Learn the "S" of the S.O.L.I.D design principles.

# ----------------------------------------------------------------------------
#     (S) Single Responsibility
#
#     A class, function, method or module should have a single responsibility.
#     If it has many responsibilities, it increases the possibility of bugs!
# ----------------------------------------------------------------------------

# Our class, SpriteGenerator, only has one responsibility - to generate sprites!
# Each class method is responsible for generating a specific type of sprite.

# For this task, implement `generate_sprite_with_item_property` method.


class SpriteGenerator:
    """
    A class to generate sprites.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the SpriteGenerator class.
        (Our SpriteGenerator does not have any attributes...yet.)
        """
        pass

    def generate_basic_sprite(self, file_path: str) -> arcade.Sprite:
        """
        This method takes in a filepath to an image (str) as input
        and returns a sprite instance.
        """
        return arcade.Sprite(file_path)

    def generate_sprite_with_item_property(
        self, file_path: str, item: str
    ) -> arcade.Sprite:
        """
        This method takes in a filepath to an image (str) and an item (str) as input
        and returns a sprite instance with the item as a custom property.

        Instantiate a sprite (https://api.arcade.academy/en/stable/api/sprites.html#arcade-sprite):
          sprite = arcade.Sprite(file_path)

        Add a custom property (https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite.properties):
          sprite.properties = { key: value }
        """
        # TODO: implement this method
        pass


# Working solution (will remove later):
#
# def generate_sprite_with_item_property(self, file_path: str, item: str):
#     sprite = arcade.Sprite(file_path)
#     sprite.properties = {'item': item}
#     return sprite
