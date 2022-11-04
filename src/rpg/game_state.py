import pickle
from pathlib import Path

from .constants import SAVE_FILE


class GameState():
  """
  Class to manage game state.
  """

  def __init__(self, player):
    self.player = player

  def get_data(self):
    path = Path(SAVE_FILE)
     # If there is save data
    if path.is_file():
      with open(SAVE_FILE, 'rb') as f:
        return pickle.load(f)
    # Otherwise, create file
    with open(SAVE_FILE, 'wb'):
      return None

  def save_data(self):
    center_x = self.player.center_x
    center_y = self.player.center_y
    data = {
      'x': center_x,
      'y': center_y,
    }
    with open(SAVE_FILE, 'wb') as f:
      pickle.dump(data, f)
