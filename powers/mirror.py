from imports.player import *

class mirror(player):
  def __init__(self, n, ident, pps, spp, crd):
    super().__init__(n, ident, pps, spp, crd)
    self.oppoRevealBool = True
    self.mirror = False

  def rev(self, n):
    if n < 10:
      result = "0"
    else:
      result = ""
    result += str(n)
    return int(result[::-1])

  def revealMath(self, aV):
    aV[0] = self.rev(aV[0])
    return super().revealMath(aV)

  def oppoReveal(self,oppo,crd, pNum):
    # [0] = card
    # [1] = number of ships
    # [2] = total allies
    # [3] = total power
    # [4] = hash of individual ally ship numbers
    attackValue = [0]*5
    if crd == 99:
      attackValue[0] = "N"
    else:
      attackValue[0] = crd

    attackValue[4] = {}

    if pNum == -1:
      aC = 0
      for x in players:
        if x == oppo:
          attackValue[1] = mothership[x]
        else:
          aC += x.shipWorth(mothership[x])
          attackValue[4][x] = mothership[x]
      attackValue[2] = aC
    else:
      attackValue[1] = oppo.system.planet[int(pNum[0])].ships[oppo]
      aC = 0
      for x in players:
        aC += x.shipWorth(carriership[x])
        attackValue[4][x] = carriership[x]
      attackValue[2] = aC

    return self.oppoRevealMath(oppo, attackValue)

  def oppoRevealMath(self, oppo, aV):
    aV[0] = self.rev(aV[0])
    return oppo.revealMath(aV)
