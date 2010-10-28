from imports.player import *

class mirror(player):
  def __init__(self, n, ident, pps, spp, crd):
    super().__init__(n, ident, pps, spp, crd)
    self.oppoRevealBool = True
    self.mirror = False

  def

  def rev(x):
    result=0
    i=0
    while x/10 > 0:
      result = (result * 10) + (x % 10)
      x = x/10
    result = (result * 10) + (x % 10)
    return result
