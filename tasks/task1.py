import arcade


def generate_sprite(item):
    """
    This function takes in an item (string) as input and
    returns a sprite instance with the item as a custom property 

    Instantiate a sprite (https://api.arcade.academy/en/stable/api/sprites.html#arcade-sprite):
        sprite = arcade.Sprite(file_path)

    Add a custom property (https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite.properties):
        sprite.properties = { key: value }
    """
    file_path = f":misc:{item}.png"

# Notes:
#
# Currently the instructions are in the docstring, but I will move them to a google doc later
#
# Working solution below:
#
# def generate_sprite(item):
#     file_path = f":misc:{item}.png"
#     sprite = arcade.Sprite(file_path)
#     sprite.properties = {'item': item}
#     return sprite
