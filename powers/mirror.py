from imports.player import *

class mirror(player):
  def __init__(self, g, n, ident, pps, spp, crd):
    super().__init__(g, n, ident, pps, spp, crd)
    self.oppoRevealBool = True
    self.mathOverride = False

  def rev(self, n):
    if n < 10:
      result = "0"
    else:
      result = ""
    result += str(n)
    return int(result[::-1])

  def powerMath(self, aV):
    if aV[0] != "N":
      aV[0] = self.rev(aV[0])
      aV[3] = aV[0] + aV[1] + aV[2]
    return aV

  def beforeCardsChosen(self, theGame, plyr, oppo):
    if self == plyr or self == oppo:
      while 1:
        checkMirror = input(self.name+">> Would you like to mirror? [y/n]: ")
        if checkMirror.lower() == "n":
          self.mathOverride = False
          return 0
        elif checkMirror.lower() == "y":
          self.mathOverride = True
          return 0
        else:
          print("Whoa there, buddy! You need to input an answer in a correct format!")
