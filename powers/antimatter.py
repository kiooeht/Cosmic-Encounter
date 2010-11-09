from imports.player import *

class antimatter(player):
  def __init__(self, g, n, ident, pps, spp, crd):
    super().__init__(g, n, ident, pps, spp, crd)
    self.mathOverrideOppo = True

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] - aV[1] - aV[2]
    else:
      aV[3] = "N"

    return aV

  def powerMath(self, aV):
    if aV[0] != "N":
      aV[3] -= 2 * aV[2]
    else:
      aV[3] = "N"

    return aV
