from imports.artifact import *
from imports.drawing import draw

class quash(artifact):
  def __init__(self, g):
    super().__init__(g, "Quash", "QA", "resolution")

  def use(self, plyr, crd, other):
    oppo = other[0]
    res = other[1]
    success = other[2]
    if res[0] == "N" and res[1] == "N" and success[0]:
      print("The deal has been Quashed")
      success[0] = False
      print("Pick 3 ships to kill")
      draw(self.theGame)
      print(plyr.name+">>\t",end='')
      self.theGame.carriership[plyr] += plyr.getShips(3, 3)
      print(oppo.name+">>\t",end='')
      self.theGame.carriership[oppo] += oppo.getShips(3, 3)

      plyr.killShips(3, self.theGame.carriership, plyr)
      oppo.killShips(3, self.theGame.carriership, oppo)
      super().use(plyr, crd, other)
    else:
      print("No deal to be Quashed")
