from imports.player import *

class trader(player):
  def beforeCardsChosen(self, theGame, plyr, oppo):
    if not self.hasPower or self.zapped:
      return super().beforeCardsChosen(theGame, plyr, oppo)
    else:
      if self == plyr or self == oppo:
        if self == plyr: switch = oppo
        elif self == oppo: switch = plyr
        while 1:
          trade = input(self.name+">> Trade hands with other player? [y/n]: ")
          if trade.lower() == "y":
            spare = self.hand
            self.hand = switch.hand
            switch.hand = spare
            return 1
          elif trade.lower() == "n":
            return 0
          else:
            print("ERROR: YOU FAIL")
