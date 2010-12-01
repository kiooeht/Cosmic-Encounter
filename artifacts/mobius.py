from imports.artifact import *
from imports.drawing import draw

class mobius(artifact):
  def __init__(self, g):
    super().__init__(g, "Mobius Tubes", "MT", "start turn")

  def use(self, plyr, crd, other):
    print("All ships in warp returned to players")
    worked = super().use(plyr, crd, other)

    if worked:
      for x in self.theGame.warp:
        if self.theGame.warp[x] > 0:
          print(x.name+">> "+str(self.theGame.warp[x])+" ship(s) back")
          draw(self.theGame)
          x.placeShips(self.theGame.warp[x])
          self.theGame.warp[x] = 0
