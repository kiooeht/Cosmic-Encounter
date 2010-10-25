from imports.player import *

class trader(player):
  def beforeCardsChosen(self, oppo):
    while 1:
      trade = input(self.name+">> Trade hands with other player? [y/n]: ")
      if trade.lower() == "y":
        spare = self.hand
        self.hand = oppo.hand
        oppo.hand = spare
        return 1
      elif trade.lower() == "n":
        return 0
      else:
        print("ERROR: YOU FAIL")
