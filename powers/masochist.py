from imports.player import *

class masochist(player):
  def checkWin(self):
    if not self.hasPower or self.zapped:
      return super().checkWin()
    else:
      if self.getColonies() >= 5 or self.getShipCount() <= 0:
        return True
      else:
        return False

  def checkPower(self):
    self.hasPower = True
    return self.hasPower
