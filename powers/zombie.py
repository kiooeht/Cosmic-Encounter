from imports.player import *
from imports.drawing import draw

class zombie(player):
  def killShips(self, num, loc, locN):
    if not self.hasPower or self.zapped:
      super().killShips(num, loc, locN)
    else:
      loc[locN] -= num
      draw(self.theGame)
      self.placeShips(num)
