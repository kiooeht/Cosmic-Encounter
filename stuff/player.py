import sys
import random
import time

from .system import *
from .planet import *
from .globals import *

class player:
  def __init__(self, n, ident, pps, spp, crd):
    self.num  = n
    self.name   = ident
    self.system = system(self, pps, spp)
    self.hand = []
    self.drawHand(crd)

  def getShipCount(self):
    n = 0
    for x in players:
      n += x.system.getShipCount(self)
    return n

  def getWarpCount(self):
    if self in warp:
      return warp[self]
    else:
      return 0

  def getColonies(self):
    n = 0
    for x in players:
      if x != self:
        for y in x.system.planet:
          if self in y.ships:
            if y.ships[self] > 0: n += 1
    return n

  def getPlanets(self):
    n = 0
    for x in self.system.planet:
      if x.ships[self] != 0:
        n += 1
    return n

  def getOccupied(self):
    occ = []
    for x in self.system.planet:
      if x.ships[self] != 0: occ.append(x)
    for x in players:
      if x != self:
        for y in x.system.planet:
          if self in y.ships:
            if y.ships[self] > 0: occ.append(y)
    return occ

  def getStats(self):
    stats = []
    stats.append(self.getShipCount())
    stats.append(self.getWarpCount())
    stats.append(self.getColonies())
    stats.append(self.getPlanets())
    stats.append(len(self.hand))
    return stats

  def showHand(self):
    l = len(self.hand)
    lt = len(self.hand)
    while lt >= 7:
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write(str(x))
        if x < 10: sys.stdout.write("-")
        sys.stdout.write("---+ ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("|    | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("| ")
        if self.hand[x] == 99: sys.stdout.write("N ")
        else:
          if self.hand[x] < 10: sys.stdout.write("0")
          sys.stdout.write(str(self.hand[x]))
        sys.stdout.write(" | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("|    | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("+----+ ")
      print("")
      lt -= 7
    if lt != 0:
      for x in range(l-lt,l):
        sys.stdout.write(str(x))
        if x < 10: sys.stdout.write("-")
        sys.stdout.write("---+ ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("|    | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("| ")
        if self.hand[x] == 99: sys.stdout.write("N ")
        else:
          if self.hand[x] < 10: sys.stdout.write("0")
          sys.stdout.write(str(self.hand[x]))
        sys.stdout.write(" | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("|    | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("+----+ ")
      print("")

  def drawHand(self,n):
    self.hand = []
    self.drawCards(n)

  def drawCards(self,n):
    self.hand.extend(cards.drawCard(n))
    self.hand.sort()

  def discardCard(self,crd):
    cards.discardCard(self.hand.pop(crd))

  def useCard(self,crd):
    return self.hand.pop(crd)

  def getCard(self,crd):
    self.hand.append(crd)

  def getCompensation(self,plyr,n):
    random.seed(time.gmtime())
    for x in range(0, n):
      crd = int(random.random()*len(plyr.hand))
      self.getCard(plyr.useCard(crd))

  def colonize(self,plnt,shps):
    plnt.editShips(self,shps)

  def getShips(self,minimum,maximum):
    n = 0
    shps = []
    done = False
    while n < maximum and not done:
      choice  = input("System, Planet, and Number of Ships (space deliminated): ")
      lst   = choice.split(" ")
      yay   = 1
      for x in range(0,len(lst)):
        if not lst[x].isdigit():
          yay = 0
          break
      if yay == 0: print("ERROR: use ints, good sir")
      else:
        for x in range(0,len(lst)): lst[x] = int(lst[x])
        if len(lst) == 3:
          if lst[0] <= len(players)-1:
            if lst[1] <= len(players[lst[0]].system.planet)-1:
              if n + lst[2] <= maximum:
                if self in players[lst[0]].system.planet[lst[1]].ships:
                  if players[lst[0]].system.planet[lst[1]].ships[self] >= lst[2]:
                    n += lst[2]
                    players[lst[0]].system.planet[lst[1]].editShips(self,lst[2]*-1)
                  else:   print("Not enough ships on this planet")
                else:     print("You do not have a colony there.")
              else:       print("You have selected more ships than you're allowed")
            else:         print("That planet does not exist in this system")
          else:           print("That system does not exist")
        else:             print("Wrong number of arguments")
      if n == maximum:  break
      if n >= minimum:
        dne = input("You have selected "+str(n)+" ships, would you like to select more? [Y/n]: ")
        if dne.lower() == "n": break
    return n

  def placeShips(self,n):
    while n > 0:
      choice  = input("System, Planet, and Number of Ships (space deliminated): ")
      lst   = choice.split(" ")
      yay   = 1
      for x in range(0,len(lst)):
        if not lst[x].isdigit():
          yay = 0
          break
      if yay == 0: print("ERROR: use ints, good sir")
      else:
        for x in range(0,len(lst)): lst[x] = int(lst[x])
        if len(lst) == 3:
          if lst[0]  <= len(players)-1:
            if lst[1] <= len(players[lst[0]].system.planet)-1:
              if lst[2] <= n:
                if self in players[lst[0]].system.planet[lst[1]].ships:
                  if players[lst[0]].system.planet[lst[1]].ships[self] > 0:
                    n -= lst[2]
                    players[lst[0]].system.planet[lst[1]].editShips(self,lst[2])
                  else:   print("You do not have a colony there.")
                else:     print("You do not have a colony there.")
              else:       print("You cannot place that many ships there")
            else:         print("That planet does not exist in this system")
          else:           print("That system does not exist")
        else:             print("Wrong number of arguments")


################################################################################
########## - GAME LOOP FUNCTIONS - #############################################
################################################################################

# Game Setup
  def gameSetup(self):
    print("Game Setup")

# Start Turn
  def startTurn(self):
    print("Start Turn")

# Regroup
  def regroup(self):
    print("Regroup")

# Destiny
  def destiny(self):
    print("Destiny")

# Launch
  def launch(self):
    print("Launch")

# Alliances
  def allyAsk(self):
    print("Asking for Allies")

  def confirmAlly(self):
    print("Someone asked you to be Allies")

# Planning
  def planning(self):
    print("Planning")

# Reveal
  def reveal(self,crd, pNum):
    attackValue = [0]*4
    if crd == 99:
      attackValue[0] = "N"
    else:
      attackValue[0] = crd

    if pNum == -1:
      aC = 0
      for x in players:
        if x == self:
          attackValue[1] = mothership[x]
        else:
          aC += mothership[x]
      if attackValue[0] != "N":
        attackValue[2] = aC
    else:
      attackValue[1] = self.system.planet[int(pNum)].ships[self]
      aC = 0
      for x in players:
        aC += carriership[x]
      if attackValue[0] != "N":
        attackValue[2] = aC

    return self.revealMath(attackValue)

  def revealMath(self, aV):
    print("boo")
    if aV[0] != "N":
      aV[3] = aV[0] + aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV

# Resolution
  def resolution(self):
    print("Resolution")
