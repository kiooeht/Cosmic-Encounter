from imports.artifact import *
from imports.drawing import draw

class forcefield(artifact):
  def __init__(self, g):
    super().__init__(g, "Force Field", "FF", "alliance")

  def use(self, plyr):
    print("yay")
    for x in self.theGame.mothership:
      if x != "owner":
        if x != self.theGame.players[self.theGame.plyrix]:
          if self.theGame.mothership[x] > 0:
            print(x.name+">>")
            draw(self.theGame)
            x.placeShips(self.theGame.mothership[x])
            self.theGame.mothership[x] = 0
    for x in self.theGame.carriership:
      if self.theGame.carriership[x] > 0:
        print(x.name+">>")
        draw(self.theGame)
        x.placeShips(self.theGame.carriership[x])
        self.theGame.carriership[x] = 0
