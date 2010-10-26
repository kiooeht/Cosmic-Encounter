import random
import time

from imports.player import *
from imports.globals import mothership

class mite(player):
  def launch(self,dest):
    choice = super().launch(dest)

    if len(choice[1].hand) > 3:
      while 1:
        miteChoice = input(choice[1].name+">> Discard down to 3 cards or give "+self.name+" a colony? [3/c]: ")
        if miteChoice == "3":
          for x in range(0, len(choice[1].hand)-3):
            random.seed(time.gmtime())
            crd = int(random.random()*len(choice[1].hand))
            choice[1].discardCard(crd)
          break
        elif miteChoice.lower() == "c":
          planet = dest.system.planet[int(choice[0])]
          self.colonize(planet, mothership[self])
          choice = "successful"
          break
        else:
          print("ERROR: NOT AN OPTION")

    return choice
