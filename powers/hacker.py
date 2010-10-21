from imports.player import *
from imports.drawing import printStats
from imports.globals import players

class hacker(player):
  def getCompensation(self,plyr,n):
    printStats()
    plyr = input("Who would you like to take compensation from? (number): ")
    plyr = players[int(plyr)]
    for x in range(0, n):
      plyr.showHand()
      print("You can take "+ (n-x) +" more cards")
      crd = input("Select card to take [0-"+str(len(plyr.hand)-1)+"]: ")
      self.getCard(plyr.giveCompensation(crd))

  def giveCompensation(self, crd):
    while 1:
      self.showHand()
      selCard = input("Select a card to give as compensation [0-"+str(len(self.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(self.hand)-1 and int(selCard) >= 0:
        giveCard = self.useCard(int(selCard))
        break
      else:
        print("That does not exist in your hand")
    return giveCard
