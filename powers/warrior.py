from imports.player import *

class warrior(player):
  def __init__(self, g, n, ident, pps, spp, crd):
    super().__init__(g, n, ident, pps, spp, crd)
    self.tokens = 0

  def winEncounter(self, off, dest, choice):
    super().winEncounter(off, dest, choice)
    if self.hasPower:
      self.tokens += 1

  def loseEncounter(self, off, dest, choice):
    super().loseEncounter(off, dest, choice)
    if self.hasPower:
      self.tokens += 2

  def revealMath(self, aV):
    if not self.hasPower or self.zapped:
      return super().revealMath(aV)
    else:
      if aV[0] != "N":
        aV[3] = aV[0] + aV[1] + aV[2] + self.tokens
      else:
        aV[3] = "N"

      return aV
