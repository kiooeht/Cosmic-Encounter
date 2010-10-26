import sys
import random
import time

from .system  import *
from .planet  import *
from .globals import *
from .drawing import draw

class player:
  def __init__(self, n, ident, pps, spp, crd):
    self.num    = n
    self.name   = ident
    self.system = system(self, pps, spp)
    self.hand   = []
    self.initialHand = crd
    self.drawHand(self.initialHand)
    self.encounterNumber = 1
    self.oppoRevealBool = False

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

  def discardECard(self,crd):
    cards

  def discardHand(self):
    for x in range(0, len(self.hand)):
      discardCard(x)

  def useCard(self,crd):
    return self.hand.pop(crd)

  def getCard(self,crd):
    self.hand.append(crd)

  def getCompensation(self,plyr,n):
    if len(plyr.hand) <= n:
      for x in range(0, len(plyr.hand)):
        self.getCard(plyr.giveCompensation(x))
    else:
      for x in range(0, n):
        random.seed(time.gmtime())
        crd = int(random.random()*len(plyr.hand))
        self.getCard(plyr.giveCompensation(crd))

  def giveCompensation(self, crd):
    return self.hand.pop(crd)

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
      print(str(n)+" ships left to place")
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

  def killShips(self, num, loc, locN):
    warp[self] += num
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
      if x < 90 or x == 99:
        return True
    return False

  def isEncounterCard(self, crd):
    return self.hand[crd] < 90 or self.hand[crd] == 99



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
    if self.getWarpCount() > 0:
      warp[self] -= 1
      mothership[self] += 1

# Destiny
  def destiny(self,desCards):
    dest = None
    while 1:
      if len(desCards.cards) == 1:
        print("Reshuffling destiny deck")
      dest = desCards.drawCard(1)[0]
      desCards.discardCard(dest)
      print("Destiny card: "+dest.name)
      if dest.name == self.name:
        attack = input("Would you like to attack your own system? [y/N]: ")
        if attack.lower() == "y":
          break
      else:
        break
    print("Attacking "+dest.name+"'s system")
    return dest

# Launch
  def launch(self,dest):
    dest.system.draw()
    choice = input("Pick a planet number: ")
    while not choice.isdigit() or int(choice) > len(dest.system.planet)-1 or int(choice) < 0:
      print("ERROR: YOU SUCK")
      choice = input("Pick a planet number: ")

    colony = dest
    if dest == self:
      # check if planet is empty
      empty = True
      for x in self.system.planet[int(choice)].ships:
        if x != 0:
          empty = False
          break
      if empty: return "successful"

      # choose colony to attack
      while 1:
        colonyNum = input("Pick a player to attack on that planet (number [0-"+str(len(players)-1)+"]): ")
        if colonyNum.isdigit() and int(colonyNum) < len(players) and int(colonyNum) >= 0:
          if players[int(colonyNum)] == self:
            print("You can't attack your own colony!")
          elif players[int(colonyNum)] not in self.system.planet[int(choice)].ships:
            print("That player does not have a colony there!")
          elif self.system.planet[int(choice)].ships[players[int(colonyNum)]] == 0:
            print("That player does not have a colony there!")
          else:
            colony = players[int(colonyNum)]
            break

    # choose ships
    draw()
    if mothership[self] != 0:
      mothership[self] += self.getShips(0,4-mothership[self])
    else:
      mothership[self] += self.getShips(1,4)
    return [choice, colony]

# Alliances
  def allyAsk(self,oppent):
    allies = []
    if len(players) - 2 > 0:
      askHelp = input(self.name+", Would you like to ask for allies? [Y/n]: ")
      if askHelp.lower() != "n":
        for x in players:
          if x != self and x != oppent:
            plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            while plyHelp.lower() != "y" and plyHelp.lower() != "n":
              print("Excuse me, sir/madam, but it appears that you have neglected to specify")
              print("correctly a positive or negative response to my question. If you would")
              print("be so gracious, would you please try again and don't mess up this time.")
              print("Thank you.")
              plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            if plyHelp.lower() == "y":
              allies.append(x)
    return allies

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
  def planning(self,dest):
    ##offense
    print(self.name+">>")
    if len(self.hand) <= 0:
      self.drawHand(self.initialHand)
      print("Drawing a new hand")
    # check if player has an encounter card
    while not self.hasEncounterCards():
      self.discardHand()
      self.drawHand(self.initialHand)
      print("No encounter cards left, drawing a new hand")
    # Do any power stuff that should be before chosing cards
    self.beforeCardsChosen(dest)
    dest.beforeCardsChosen(self)
    print(self.name+">>")
    while 1:
      self.showHand()
      selCard = input("Select an encounter card from your hand [0-"+str(len(self.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(self.hand)-1 and int(selCard) >= 0:
        # check if card is encounter card
        if self.isEncounterCard(int(selCard)):
          offCard = self.useCard(int(selCard))
          break
        else:
          print("That is not an encounter card")
      else:
        print("That does not exist in your hand")
    ##defense
    print(dest.name+">>")
    if len(dest.hand) <= 0:
      dest.drawHand(self.initialHand)
      print("Drawing a new hand")
    # check if player has an encounter card
    if not dest.hasEncounterCards():
      dest.discardHand()
      dest.drawHand(self.initialHand)
      print("No encounter cards left, drawing a new hand")
    while 1:
      dest.showHand()
      selCard = input("Select an encounter card from your hand [0-"+str(len(dest.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(dest.hand)-1 and int(selCard) >= 0:
        # check if card is encounter card
        if dest.isEncounterCard(int(selCard)):
          defCard = dest.useCard(int(selCard))
          break
        else:
          print("That is not an encounter card")
      else:
        print("That does not exist in your hand")
    return [offCard,defCard]

  def beforeCardsChosen(self, oppo):
    # Do nothing
    return 0

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
      attackValue[1] = self.system.planet[int(pNum[0])].ships[self]
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
  def resolution(self, oppo, res, plan, choice):
    if str(res[0]) != "N" and str(res[1]) != "N":
      if res[0] > res[1]:
        successful = True
        self.winEncounter(self, oppo, choice)
        oppo.loseEncounter(self, oppo, choice)
      else:
        successful = False
        self.loseEncounter(self, oppo, choice)
        oppo.winEncounter(self, oppo, choice)
    else:
      if str(res[1]) == "N":
        successful = True
        oppo.getCompensation(self, oppo.system.planet[int(choice[0])].ships[oppo])
        self.winEncounter(self, oppo, choice)
        oppo.loseEncounter(self, oppo, choice)
      elif str(res[0]) == "N":
        successful = False
        self.getCompensation(oppo, mothership[self])
        self.loseEncounter(self, oppo, choice)
        oppo.winEncounter(self, oppo, choice)

    self.discardUsedECard(plan[0])
    oppo.discardUsedECard(plan[1])
    return successful

  def discardUsedECard(self, crd):
    cards.discardCard(crd)

  def winEncounter(self, off, dest, choice):
    if self == off:
      ## colonize
      off.colonize(dest.system.planet[int(choice[0])], mothership[off])
      mothership[off] = 0
      ## return offense allies
      for x in players:
        x.placeShips(mothership[x])
        mothership[x] = 0
    elif self == dest:
      ## return defense allies
      for x in players:
        ## defender reward
        if carriership[x] > 0:
          x.drawCards(carriership[x])
        x.placeShips(carriership[x])
        carriership[x] = 0

  def loseEncounter(self, off, dest, choice):
    if off != dest:
      if self == off:
        ## kill offense ships/allies
        for x in players:
          x.killShips(mothership[x], mothership, x)

      elif self == dest:
        ## kill defense allies
        for x in players:
          x.killShips(carriership[x], carriership, x)
        ## kill defense ships
        dest.killShips(dest.system.planet[int(choice[0])].ships[dest], dest.system.planet[int(choice[0])].ships, dest)
    #else:


  # Ending
  def checkWin(self):
    if self.getColonies() >= 5:
      return True
    else:
      return False
