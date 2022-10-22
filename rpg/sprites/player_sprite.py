import arcade

from rpg.sprites.character_sprite import CharacterSprite, Direction


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")
        self.item = None

    def equip(self, index):
        if len(self.inventory) > index:
            if self.item and self.item == self.inventory[index]:
                self.item = None
            else:
                self.item = self.inventory[index]
                self.item.center_x = self.center_x
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
