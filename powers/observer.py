from imports.player import *

class observer(player):
  def loseEncounter(self, off, dest, choice):
    if off != dest:
      if self == off:
        ## kill offense ships but not allies
        off.killShips(self.theGame.mothership[self], self.theGame.mothership, self)

      elif self == dest:
        ## kill defense ships but not allies
        dest.killShips(choice[2].system.planet[int(choice[0])].ships[dest], choice[2].system.planet[int(choice[0])].ships, dest)

  def killShips(self, num, loc, locN):
    if loc == self.theGame.carriership:
      draw(self.theGame)
      self.placeShips(num)
      loc[locN] = 0
    else:
      self.theGame.warp[self] += num
      loc[locN] -= num
