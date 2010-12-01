import sys
import random
import time

from .system  import *
from .planet  import *
from .drawing import draw

class player:
  def __init__(self, g, n, ident, pps, spp, crd):
    self.theGame= g
    self.num    = n
    self.name   = ident
    self.system = system(self.theGame, self, pps, spp)
    self.initialPlanets = pps
    self.hand   = []
    self.initialHand = crd
    self.drawHand(self.initialHand)
    self.encounterNumber = 1
    self.hasPower = True
    self.zapped = False
    self.mathOverrideSelf = False
    self.mathOverrideOppo = False
    self.calcWin = False

  def getPower(self):
    return self.__class__.__name__

  def getShipCount(self):
    n = 0
    for x in self.theGame.players:
      n += x.system.getShipCount(self)
    return n

  def getWarpCount(self):
    if self in self.theGame.warp:
      return self.theGame.warp[self]
    else:
      return 0

  def getColonies(self):
    n = 0
    for x in self.theGame.players:
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
    for x in self.theGame.players:
      if x != self:
        for y in x.system.planet:
          if self in y.ships:
            if y.ships[self] > 0: occ.append(y)
    return occ

  def getStats(self):
    stats = []
    stats.append(self.getPower())
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
        if self.hand[x] == 90:
          sys.stdout.write("N ")
        elif self.hand[x] > 90:
          sys.stdout.write(self.theGame.artDef[self.hand[x]].short)
        else:
          if self.hand[x] < 10: sys.stdout.write("0")
          sys.stdout.write(str(self.hand[x]))
        sys.stdout.write(" | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("|    | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("+----")
        if self.hand[x] > 90:
          sys.stdout.write("A ")
        else:
          sys.stdout.write("+ ")
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
        if self.hand[x] == 90:
          sys.stdout.write("N ")
        elif self.hand[x] > 90:
          sys.stdout.write(self.theGame.artDef[self.hand[x]].short)
        else:
          if self.hand[x] < 10: sys.stdout.write("0")
          sys.stdout.write(str(self.hand[x]))
        sys.stdout.write(" | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("|    | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("+----")
        if self.hand[x] > 90:
          sys.stdout.write("A ")
        else:
          sys.stdout.write("+ ")
      print("")

  def drawHand(self,n):
    self.hand = []
    self.drawCards(n)

  def drawCards(self,n):
    self.hand.extend(self.theGame.cards.drawCard(n))
    self.hand.sort()

  def discardCard(self,crd):
    self.theGame.cards.discardCard(self.hand.pop(crd))

  def discardECard(self,crd):
    self.theGame.cards.discard(crd)

  def discardHand(self):
    for x in range(0, len(self.hand)):
      self.discardCard(x)

  def useCard(self,crd):
    return self.hand.pop(crd)

  def getCard(self,crd):
    self.hand.append(crd)
    self.hand.sort()

  def getCompensation(self,plyr,n):
    if len(plyr.hand) > 0:
      if len(plyr.hand) <= n:
        self.hand.extend(plyr.hand)
        plyr.hand = []
      else:
        for x in range(0, n):
          random.seed(time.gmtime())
          crd = int(random.random()*len(plyr.hand))
          self.getCard(plyr.giveCompensation(crd))
      self.hand.sort()

  def giveCompensation(self, crd):
    return self.hand.pop(crd)

  def checkArtifacts(self, phase, *other):
    num = 0
    for x in self.hand:
      if x > 90:
        for p in self.theGame.artDef[x].phases:
          if p == phase:
            while 1:
              useArt = input(self.name+">> Would you like to use "+ \
                             self.theGame.artDef[x].name + "? [y/N]: ")
              if useArt.lower() == "y":
                self.theGame.artDef[x].use(self, num, other)
                break
              elif useArt.lower() == "n" or useArt == "":
                break
              else:
                print("WTF? Use proper answers")
      num += 1

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
          if lst[0] <= len(self.theGame.players)-1:
            if lst[1] <= len(self.theGame.players[lst[0]].system.planet)-1:
              if n + lst[2] <= maximum:
                if self in self.theGame.players[lst[0]].system.planet[lst[1]].ships:
                  if self.theGame.players[lst[0]].system.planet[lst[1]].ships[self] >= lst[2]:
                    n += lst[2]
                    self.theGame.players[lst[0]].system.planet[lst[1]].editShips(self,lst[2]*-1)
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
      print(str(n)+" ships left to place")
      choice  = input("System, Planet, and Number of Ships (space deliminated): ")
      lst     = choice.split(" ")
      yay     = 1
      for x in range(0,len(lst)):
        if not lst[x].isdigit():
          yay = 0
          break
      if yay == 0: print("ERROR: use ints, good sir")
      else:
        for x in range(0,len(lst)): lst[x] = int(lst[x])
        if len(lst) == 3:
          if lst[0]  <= len(self.theGame.players)-1:
            if lst[1] <= len(self.theGame.players[lst[0]].system.planet)-1:
              if lst[2] <= n:
                if self in self.theGame.players[lst[0]].system.planet[lst[1]].ships:
                  if self.theGame.players[lst[0]].system.planet[lst[1]].ships[self] > 0:
                    n -= lst[2]
                    self.theGame.players[lst[0]].system.planet[lst[1]].editShips(self,lst[2])
                  else:   print("You do not have a colony there.")
                else:     print("You do not have a colony there.")
              else:       print("You cannot place that many ships there")
            else:         print("That planet does not exist in this system")
          else:           print("That system does not exist")
        else:             print("Wrong number of arguments")

  def moveShips(self):
    draw(self.theGame)
    while 1:
      move = input("Would you like to move ships around? [y/N]: ")
      if move.lower() == "n" or move == "":
        break
      elif move.lower() == "y":
        n = self.getShips(0, self.getShipCount())
        self.placeShips(n)
      else:
        print("Pick y or n")

  def killShips(self, num, loc, locN):
    self.theGame.warp[self] += num
    loc[locN] -= num

  def goAgain(self, success):
    if success and self.encounterNumber < 2:
      while 1:
        again = input("Would you like to have another encounter? [Y/n]: ")
        if again.lower() == "y" or again.lower() == "":
          self.encounterNumber += 1
          return True
        elif again.lower() == "n":
          self.encounterNumber = 1
          return False
        else:
          print("ERROR: Try again")
    else:
      self.encounterNumber = 1
      return False

  def hasEncounterCards(self):
    for x in self.hand:
      if x <= 90:
        return True
    return False

  def isEncounterCard(self, crd):
    return self.hand[crd] <= 90

  def maxShipsPerLoad(self):
    return 4



################################################################################
########## - GAME LOOP FUNCTIONS - #############################################
################################################################################

# Game Setup
  def gameSetup(self):
    print("Game Setup")

# Start Turn
  def startTurn(self):
    print("Start Turn")

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
          draw(self.theGame)
          print("Ships for Offense")
          mothership[self] = self.getShips(1,self.maxShipsPerLoad())

          draw(self.theGame)
          print("Ships for Defense")
          carriership[self] = self.getShips(1,self.maxShipsPerLoad())
        else:
          print("You have chosen to help the ",end='')
          if helping == offP:
            print("Offense ("+helping.name+")")
            draw(self.theGame)
            self.theGame.mothership[self] = self.getShips(1,self.maxShipsPerLoad())
          else:
            print("Defense ("+helping.name+")")
            draw(self.theGame)
            self.theGame.carriership[self] = self.getShips(1,self.maxShipsPerLoad())

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0] + aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV

  def shipWorth(self, num):
    return num * 1

  def discardUsedECard(self, crd):
    self.theGame.cards.discardCard(crd)

  def winEncounter(self, off, dest, choice):
    if self == off:
      if self == choice[2]:
        ## place ships where ever
        draw(self.theGame)
        self.placeShips(self.theGame.mothership[self])
        self.theGame.mothership[self] = 0
      else:
        ## colonize
        off.colonize(choice[2].system.planet[int(choice[0])], self.theGame.mothership[off])
        self.theGame.mothership[off] = 0
      ## return offense allies
      for x in self.theGame.players:
        if self.theGame.carriership[x] > 0:
          draw(self.theGame)
          x.placeShips(self.theGame.mothership[x])
          self.theGame.mothership[x] = 0
    elif self == dest:
      ## return defense allies
      for x in self.theGame.players:
        ## defender reward
        if self.theGame.carriership[x] > 0:
          draw(self.theGame)
          x.drawCards(self.theGame.carriership[x])
          x.placeShips(self.theGame.carriership[x])
          self.theGame.carriership[x] = 0

  def loseEncounter(self, off, dest, choice):
    if off != dest:
      if self == off:
        ## kill offense ships/allies
        for x in self.theGame.players:
          if self.theGame.mothership[x] > 0:
            x.killShips(self.theGame.mothership[x], self.theGame.mothership, x)

      elif self == dest:
        ## kill defense allies
        for x in self.theGame.players:
          if self.theGame.carriership[x] > 0:
            x.killShips(self.theGame.carriership[x], self.theGame.carriership, x)
        ## kill defense ships
        dest.killShips(choice[2].system.planet[int(choice[0])].ships[dest], choice[2].system.planet[int(choice[0])].ships, dest)
    self.checkPower()


  # Ending
  def checkWin(self):
    if self.getColonies() >= 5:
      return True
    else:
      return False

  def checkPower(self):
    if self.getPlanets() < round(self.initialPlanets/2 + 0.5):
      self.hasPower = False
    else:
      self.hasPower = True
    return self.hasPower


###########################################
### EXTRA POWER PHASE POSSIBILITIES #######
###########################################
  def usePower(self):
    # Artifacts
    for x in self.theGame.players:
      x.checkArtifacts("power", self)

  def beforeCardsChosen(self, theGame, plyr, oppo):
    # Do nothing
    return 0

  def afterLaunch(self, theGame, plyr, dest, choice):
    return choice

  def powerMath(self, theGame, plyr, dest, attackValue):
    return 0
