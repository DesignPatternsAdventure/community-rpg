"""
Loading screen
"""
import arcade

from ..draw_bar import draw_bar
from .game_view import GameView
from .inventory_view import InventoryView
from .main_menu_view import MainMenuView
from .settings_view import SettingsView


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        if self.started:
            self.window.views["game"] = GameView()
            self.window.views["game"].setup()
            self.window.views["inventory"] = InventoryView()
            self.window.views["inventory"].setup()
            self.window.views["main_menu"] = MainMenuView()
            self.window.views["settings"] = SettingsView()
            self.window.views["settings"].setup()

            self.window.show_view(self.window.views["game"])
