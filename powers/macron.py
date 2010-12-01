from imports.player import *

class macron(player):
  def maxShipsPerLoad(self):
    if not self.hasPower or self.zapped:
      return super().maxShipsPerLoad()
    else:
      return 1

  def revealMath(self, aV):
    if not self.hasPower or self.zapped:
      return super().revealMath(aV)
    else:
      if aV[0] != "N":
        aV[3] = aV[0] + self.shipWorth(aV[1]) + aV[2]
      else:
        aV[3] = "N"

      return aV

  def shipWorth(self, num):
    if not self.hasPower or self.zapped:
      return super().shipWorth(num)
    else:
      return num * 4
