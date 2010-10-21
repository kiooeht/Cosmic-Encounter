from imports.player import *

class virus(player):
  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] * aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV
