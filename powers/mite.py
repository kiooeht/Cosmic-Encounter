import random
import time

from imports.player import *
from imports.globals import mothership

class mite(player):
  def launch(self,dest):
    choice = super().launch(dest)

    if len(dest.hand) > 3:
      while 1:
        miteChoice = input(dest.name+">> Discard down to 3 cards or give Mite a colony? [3/c]:")
        if miteChoice == "3":
          for x in range(0, len(dest.hand)-3):
            random.seed(time.gmtime())
            crd = int(random.random()*len(dest.hand))
            dest.discardCard(crd)
          break
        elif miteChoice.lower() == "c":
          planet = dest.system.planet[int(choice)]
          self.colonize(planet, mothership[self])
          choice = "successful"
          break
        else:
          print("ERROR: NOT AN OPTION")

    return choice
