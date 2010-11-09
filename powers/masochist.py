from imports.player import *

class masochist(player):
  def checkWin(self):
    if self.getColonies() >= 5 or self.getShipCount() <= 0:
      return True
    else:
      return False
