from imports.player import *
from imports.drawing import draw

class zombie(player):
  def killShips(self, num, loc, locN):
    loc[locN] -= num
    draw()
    self.placeShips(num)
