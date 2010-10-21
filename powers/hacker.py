from imports.player import *
from imports.drawing import printStats
from imports.globals import players

class hacker(player):
  def getCompensation(self,plyr,n):
    print(self.name+">>")
    while 1:
      printStats()
      plyrNum = input("Who would you like to take compensation from? [0-"+str(len(players)-1)+"]: ")
      if plyrNum.isdigit() and int(plyrNum) < len(players) and int(plyrNum) >= 0:
        if players[int(plyrNum)] == self:
          print("That is you. You can't compensate yourself.")
        else:
          plyr = players[int(plyrNum)]
          break
      else:
        print("That player does not exist")
    for x in range(0, n):
      while 1:
        plyr.showHand()
        print("You can take "+ str(n-x) +" more cards")
        crd = input("Select card to take [0-"+str(len(plyr.hand)-1)+"]: ")
        if crd.isdigit() and int(crd) < len(plyr.hand) and int(crd) >= 0:
          self.getCard(plyr.giveCompensation(int(crd)))
          break
        else:
          print("That does not exist in their hand")

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
