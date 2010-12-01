from imports.player import *

class tripler(player):
  def revealMath(self, aV):
    if not self.hasPower or self.zapped:
      return super().revealMath(aV)
    else:
      if aV[0] != "N":
        if aV[0] <= 10:
          aV[0] *= 3
        else:
          aV[0] = int(round(aV[0]/3, 0))
        aV[3] = aV[0] + aV[1] + aV[2]
      else:
        aV[3] = "N"

      return aV
