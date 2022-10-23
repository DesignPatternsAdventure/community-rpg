import arcade

from rpg.sprites.character_sprite import CharacterSprite, Direction
from rpg.message_box import MessageBox


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")
        self.item = None
        self.item_anim_frame = 0
        self.item_anim_reversed = False
        self.item_target = None

    def equip(self, index):
        if len(self.inventory) > index:
            if self.item and self.item == self.inventory[index]:
                self.item = None
            else:
                self.item = self.inventory[index]
                self.update_item_position()
        else:
            print('No item in inventory slot!')

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0

        if self.item:
            self.update_item_position()

    def update_item_position(self):
        self.item.center_y = self.center_y - 5

        if self.direction == Direction.LEFT:
            self.item.center_x = self.center_x - 10
            self.item.scale = -1
            self.item.angle = -90

        if self.direction == Direction.RIGHT:
            self.item.center_x = self.center_x + 10
            self.item.scale = 1
            self.item.angle = 0

        if self.direction == Direction.UP:
            self.item.center_x = self.center_x - 15
            self.item.scale = -1
            self.item.angle = -90

        if self.direction == Direction.DOWN:
            self.item.center_x = self.center_x + 15
            self.item.scale = 1
            self.item.angle = 0

    def add_item_to_inventory(self, view, item):
        item_name = item.properties['item']
        item_in_list = next(
            (item for item in self.inventory if item.properties['item'] == item_name),
            None
        )
        if item_in_list:
            item_in_list.properties['count'] += 1
        else:
            item.properties['count'] = 1
            self.inventory.append(item)
        view.message_box = MessageBox(
            view,
            f"{item.properties['item']} added to inventory!",
            f"Press {str(len(self.inventory))} to use item. Press any key to close this message."
        )

    def animate_item(self, view, config):
        if self.item_anim_frame < config["frames"]:
            angle = config["speed"]
            shift_x = config["shift_x"]
            shift_y = config["shift_y"]
            if self.direction == Direction.RIGHT or self.direction == Direction.DOWN:
                angle = -angle
            if config["reversable"]:
                if self.item_anim_frame % config["reverse_frame"] == 0:
                    self.item_anim_reversed = not self.item_anim_reversed
                if self.item_anim_reversed:
                    self.item.angle += angle
                    self.item.center_x -= shift_x
                    self.item.center_y -= shift_y
                else:
                    self.item.angle -= angle
                    self.item.center_x += shift_x
                    self.item.center_y += shift_y
            else:
                self.item.angle += angle
                self.item.center_x -= shift_x
                self.item.center_y -= shift_y
            self.item_anim_frame += 1
            return True
        self.item_anim_frame = 0
        if self.item_target:
            self.item_target.remove_from_sprite_lists()
            if "item" in self.item_target.properties:
                item_name = self.item_target.properties['item']
                item = arcade.Sprite(
                    f":misc:{item_name}.png"
                )
                item.properties = {'item': item_name}
                self.add_item_to_inventory(view, item)
            self.item_target = None
        return False
