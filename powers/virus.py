from imports.player import *

class virus(player):
  def revealMath(self, aV):
    self.usePower()
    if not self.hasPower or self.zapped:
      return super().revealMath(aV)
    else:
      if aV[0] != "N":
        aV[3] = aV[0] * aV[1] + aV[2]
      else:
        aV[3] = "N"

      return aV
