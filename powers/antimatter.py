from imports.player import *

class antimatter(player):
  def __init__(self, n, ident, pps, spp, crd):
    self.num  = n
    self.name   = ident
    self.system = system(self, pps, spp)
    self.hand = []
    self.drawHand(crd)
    self.oppoRevealBool = True

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] - aV[1] - aV[2]
    else:
      aV[3] = "N"

    return aV

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
      attackValue[1] = oppo.system.planet[int(pNum)].ships[oppo]
      aC = 0
      for x in players:
        aC += x.shipWorth(carriership[x])
        attackValue[4][x] = carriership[x]
      attackValue[2] = aC

    return self.oppoRevealMath(attackValue)

  def oppoRevealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] + aV[1] - aV[2]
    else:
      aV[3] = "N"

    return aV

