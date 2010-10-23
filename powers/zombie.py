from imports.player import *

class zombie(player):
  def killShips(self, num, loc, locN):
    loc[locN] -= num
    self.placeShips(num)
