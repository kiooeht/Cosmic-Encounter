import sys
import random
import time

from .system  import *
from .planet  import *
from .globals import *
from .drawing import draw

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
  def launch(self,dest):
    dest.system.draw()
    choice = input("Pick a planet number: ")
    while not choice.isdigit() or int(choice) > len(dest.system.planet)-1 or int(choice) < 0:
      print("ERROR: YOU SUCK")
      choice = input("Pick a planet number: ")
    #choose ships
    draw()
    if mothership[self] != 0:
      mothership[self] += self.getShips(0,4-mothership[self])
    else:
      mothership[self] += self.getShips(1,4)
    return choice

# Alliances
  def allyAsk(self):
    print("Asking for Allies")

  def confirmAlly(self, offP, offAskPly, defP, defAskPly):
    helping = None
    offAsked = False
    defAsked = False
    for i in offAskPly:
      if i == self:
        offAsked = True
    for i in defAskPly:
      if i == self:
        defAsked = True
    if offAsked or defAsked:
      while helping == None:
        print(self.name+">>")
        if offAsked and defAsked:
          print("  Both the Offense ("+offP.name+") and Defense ("+defP.name+") have asked for your help")
          accept = input("  Would you like to help the Offense, Defense, Both, or Neither? [o/d/b/n]: ")
          if accept.lower() == "o":
            helping = offP
          elif accept.lower() == "d":
            helping = defP
          elif accept.lower() == "b":
            helping = "both"
        elif offAsked:
          print("  The Offense ("+offP.name+") has asked for your help")
          accept = input("  Would you like to help the Offense? [y/n]: ")
          if accept.lower() == "y":
            helping = offP
        else:
          print("  The Defense ("+defP.name+") has asked for your help")
          accept = input("  Would you like to help the Defense? [y/n]: ")
          if accept.lower() == "y":
            helping = defP
        if accept.lower() == "n":
          print("  Helping no one")
          break

      if helping != None:
        helpShips= {}
        if helping == "both":
          print("You have chosen to help both the Offense ("+offP.name+") and Defense ("+defP.name+")")
          draw()
          print("Ships for Offense")
          mothership[self] = self.getShips(1,4)

          draw()
          print("Ships for Defense")
          carriership[self] = self.getShips(1,4)
        else:
          print("You have chosen to help the ",end='')
          if helping == offP:
            print("Offense ("+helping.name+")")
            draw()
            mothership[self] = self.getShips(1,4)
          else:
            print("Defense ("+helping.name+")")
            draw()
            carriership[self] = self.getShips(1,4)


# Planning
  def planning(self):
    print("Planning")

# Reveal
  def reveal(self,crd, pNum):
    # [0] = card
    # [1] = number of ships
    # [2] = total allies
    # [3] = total power
    # [4] = hash of individual ally ship numbers
    attackValue = [0]*5
    if crd == 99:
      attackValue[0] = "N"
    else:
      attackValue[0] = crd

    attackValue[4] = {}

    if pNum == -1:
      aC = 0
      for x in players:
        if x == self:
          attackValue[1] = mothership[x]
        else:
          aC += x.shipWorth(mothership[x])
          attackValue[4][x] = mothership[x]
      attackValue[2] = aC
    else:
      attackValue[1] = self.system.planet[int(pNum)].ships[self]
      aC = 0
      for x in players:
        aC += x.shipWorth(carriership[x])
        attackValue[4][x] = carriership[x]
      attackValue[2] = aC

    return self.revealMath(attackValue)

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] + aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV

  def shipWorth(self, num):
    return num * 1

# Resolution
  def resolution(self):
    if str(res[0]) != "N" and str(res[1]) != "N":
      if res[0] > res[1]:
        self.offenseWin()
      else:
        self.defenseWin()

  def winEncounter(self):
    print("you win")

  def loseEncounter(self):
    print("you lose")

