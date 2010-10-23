from imports.player import *

class masochist(player):
  def checkWin(self):
    if self.getColonies() >= 5 || self.getShipCount() <= 0:
      return True
    else:
      return False
