from imports.artifact import *
from imports.drawing import printStats, draw

class plague(artifact):
  def __init__(self, g):
    super().__init__(g, "Plague", "PL", "start turn", "regroup", "destiny", \
                        "launch", "alliance", "planning", "reveal", "resolution")

  def use(self, plyr, crd, other):
    print("Pick a player to Plague")
    while 1:
      printStats(self.theGame)
      plyrNum = input("Who would you like to Plague? [0-"+str(len(self.theGame.players)-1)+"]: ")
      if plyrNum.isdigit() and int(plyrNum) < len(self.theGame.players) and int(plyrNum) >= 0:
        plyrPlague = self.theGame.players[int(plyrNum)]
        break
      else:
        print("That player does not exist")

    print(plyrPlague.name+">> You have been Plagued!")
    print("Kill 3 ships")
    draw(self.theGame)
    self.theGame.carriership[plyrPlague] += plyrPlague.getShips(3, 3)
    plyrPlague.killShips(3, self.theGame.carriership, plyrPlague)
    print("Discard 1 card of each type (Attack, Negotiate, Artifact)")
    numCrd = [0]*3
    for x in plyrPlague.hand:
      if x < 90:    numCrd[0] += 1
      elif x == 90: numCrd[1] += 1
      elif x > 90:  numCrd[2] += 1
    if numCrd == [0]*3:
      print("No cards to discard")
    else:
      if numCrd[0] > 0:
        plyrPlague.showHand()
        while 1:
          attNum = input("Select Attack card to discard [0-"+str(len(plyrPlague.hand)-1)+"]: ")
          if attNum.isdigit() and int(attNum) < len(plyrPlague.hand) and int(attNum) >= 0:
            if plyrPlague.hand[int(attNum)] < 90:
              plyrPlague.discardCard(int(attNum))
              break
            else:
              print("That is not an Attack card")
          else:
            print("That card does not exist")
      if numCrd[1] > 0:
        plyrPlague.showHand()
        while 1:
          negNum = input("Select Negotiate card to discard [0-"+str(len(plyrPlague.hand)-1)+"]: ")
          if negNum.isdigit() and int(negNum) < len(plyrPlague.hand) and int(negNum) >= 0:
            if plyrPlague.hand[int(negNum)] == 90:
              plyrPlague.discardCard(int(negNum))
              break
            else:
              print("That is not a Negotiate card")
          else:
            print("That card does not exist")
      if numCrd[2] > 0:
        plyrPlague.showHand()
        while 1:
          artNum = input("Select Artifact card to discard [0-"+str(len(plyrPlague.hand)-1)+"]: ")
          if artNum.isdigit() and int(artNum) < len(plyrPlague.hand) and int(artNum) >= 0:
            if plyrPlague.hand[int(artNum)] > 90:
              plyrPlague.discardCard(int(artNum))
              break
            else:
              print("That is not an Artifact card")
          else:
            print("That card does not exist")
    super().use(plyr, crd, other)
