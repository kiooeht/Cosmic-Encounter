from imports.player import *

class antimatter(player):
  def __init__(self, g, n, ident, pps, spp, crd):
    super().__init__(g, n, ident, pps, spp, crd)
    self.mathOverrideOppo = True
    self.calcWin = True

  def revealMath(self, aV):
    if not self.hasPower or self.zapped:
      return super().revealMath(aV)
    else:
      if aV[0] != "N":
        aV[3] = aV[0] - aV[1] - aV[2]
      else:
        aV[3] = "N"

      return aV

  def powerMath(self, aV):
    if not self.hasPower or self.zapped:
      return aV
    else:
      if aV[0] != "N":
        aV[3] -= 2 * aV[2]
      else:
        aV[3] = "N"

      return aV

  def winCalcuation(self, res):
    if not self.hasPower or self.zapped:
      return res[0] > res[1]
    else
      return res[0] < res[1]
