from imports.player import *

class macron(player):
  def maxShipsPerLoad(self):
    return 1

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] + aV[1]*4 + aV[2]
    else:
      aV[3] = "N"

    return aV

  def shipWorth(self, num):
    return num * 4
