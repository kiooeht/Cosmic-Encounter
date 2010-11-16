from .deck import *
from .drawing import *
import powers
from artifacts import *

class game:
  def __init__(self):
    self.warp = {}
    self.players = []
    self.eCards = [0,              \
                   1,              \
                   4,4,4,4,        \
                   5,              \
                   6,6,6,6,6,6,6,  \
                   7,              \
                   8,8,8,8,8,8,8,  \
                   9,              \
                   10,10,10,10,    \
                   11,             \
                   12,12,          \
                   13,             \
                   14,14,          \
                   15,             \
                   20,20,          \
                   23,             \
                   30,             \
                   40,             \
                   90,90,90,90,90, \
                   90,90,90,90,90, \
                   90,90,90,90,90, \
                   91,91,          \
                   92,92,          \
                   93,             \
                   94]
                   # 90 = N
                   # >= 91 Reserved for Artifacts
                   # 91 = MT (Mobius Tubes)
                   # 92 = FF (Force Field)
                   # 93 = EC (Emotion Control)
                   # 94 = QA (Quash)
    self.artDef = {}
    self.artDef[90] = "N"
    self.artDef[91] = mobius.mobius(self)
    self.artDef[92] = forcefield.forcefield(self)
    self.artDef[93] = emotion.emotion(self)
    self.artDef[94] = quash.quash(self)
    self.cards   = deck(self, self.eCards)
    self.destiny = deck(self)
    self.numplyrs = 0
    self.mothership = {}
    self.carriership = {}
    self.winner = None
    self.gameover = False
    self.plyrix = 0
    # Create list of all power modules
    self.listPowers = {}
    for x in powers.__all__:
      self.listPowers[x] = __import__(x, globals(), locals(), [], 0)
    self.usedPowers = []
    self.powerOpts = "random"

########## Regroup ##########
  def regroup(self, plyr):
    if plyr.getWarpCount() > 0:
      self.warp[plyr] -= 1
      self.mothership[plyr] += 1
    plyr.moveShips()
    for x in self.players:
      if x == plyr:
        x.checkArtifacts("start turn")
      else:
        x.checkArtifacts("regroup")

########## Destiny ##########
  def destinyPhase(self, plyr, desCards):
    dest = None
    while 1:
      if len(desCards.cards) == 1:
        print("Reshuffling destiny deck")
      dest = desCards.drawCard(1)[0]
      desCards.discardCard(dest)
      print("Destiny card: "+dest.name)
      if dest.name == plyr.name:
        attack = input("Would you like to attack your own system? [y/N]: ")
        if attack.lower() == "y":
          colony_exist = False
          for x in plyr.system.planet:
            completely_empty = True
            for y in x.ships:
              if x.ships[y] > 0 and y != self:
                colony_exist = True
              if x.ships[y] > 0:
                completely_empty = False
            if completely_empty:
              colony_exist = True
          if not colony_exist:
            print("There are no colonies to purge, drawing new destiny card")
          else:
            break
      else:
        break
    print("Attacking "+dest.name+"'s system")
    return dest

########## Launch ##########
  def launch(self, plyr, dest):
    dest.system.draw()
    choice = input("Pick a planet number: ")
    while not choice.isdigit() or int(choice) > len(dest.system.planet)-1 or int(choice) < 0:
      print("ERROR: YOU SUCK")
      choice = input("Pick a planet number: ")

    colony = dest
    if dest == plyr:
      # check if planet is empty
      empty = True
      for x in plyr.system.planet[int(choice)].ships:
        if x != 0:
          empty = False
          break
      if empty: return "successful"

      # choose colony to attack
      while 1:
        colonyNum = input("Pick a player to attack on that planet (number [0-"+str(len(self.players)-1)+"]): ")
        if colonyNum.isdigit() and int(colonyNum) < len(self.players) and int(colonyNum) >= 0:
          if self.players[int(colonyNum)] == plyr:
            print("You can't attack your own colony!")
          elif self.players[int(colonyNum)] not in plyr.system.planet[int(choice)].ships:
            print("That player does not have a colony there!")
          elif plyr.system.planet[int(choice)].ships[self.players[int(colonyNum)]] == 0:
            print("That player does not have a colony there!")
          else:
            colony = self.players[int(colonyNum)]
            break

    # choose ships
    draw(self)
    print("You have "+str(self.mothership[plyr])+" ship(s) in the mothership")
    if self.mothership[plyr] != 0:
      self.mothership[plyr] += plyr.getShips(0,plyr.maxShipsPerLoad()-self.mothership[plyr])
    else:
      self.mothership[plyr] += plyr.getShips(1,plyr.maxShipsPerLoad())
    # [0] = planet number (string)
    # [1] = owner of colony (player)
    # [2] = owner of system (player)
    return [choice, colony, dest]

########## Alliances ##########
  def allyAsk(self, plyr, oppent):
    allies = []
    if len(self.players) - 2 > 0:
      askHelp = input(plyr.name+", Would you like to ask for allies? [Y/n]: ")
      if askHelp.lower() != "n":
        for x in self.players:
          if x != plyr and x != oppent:
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

########## Planning ##########
  def planning(self, plyr, dest):
    ##offense
    print(plyr.name+">>")
    if len(plyr.hand) <= 0:
      plyr.drawHand(plyr.initialHand)
      print("Drawing a new hand")
    # check if player has an encounter card
    while not plyr.hasEncounterCards():
      plyr.discardHand()
      plyr.drawHand(plyr.initialHand)
      print("No encounter cards left, drawing a new hand")
    # Do any power stuff that should be before chosing cards
    for x in self.players:
      x.beforeCardsChosen(self, plyr, dest)
    print(plyr.name+">>")
    while 1:
      plyr.showHand()
      selCard = input("Select an encounter card from your hand [0-"+str(len(plyr.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(plyr.hand)-1 and int(selCard) >= 0:
        # check if card is encounter card
        if plyr.isEncounterCard(int(selCard)):
          offCard = plyr.useCard(int(selCard))
          break
        else:
          print("That is not an encounter card")
      else:
        print("That does not exist in your hand")
    ##defense
    print(dest.name+">>")
    if len(dest.hand) <= 0:
      dest.drawHand(dest.initialHand)
      print("Drawing a new hand")
    # check if player has an encounter card
    if not dest.hasEncounterCards():
      dest.discardHand()
      dest.drawHand(dest.initialHand)
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

########## Reveal ##########
  def reveal(self, plyr, crd1, dest, crd2, pNum):
    # [0] = card
    # [1] = number of ships
    # [2] = total allies
    # [3] = total power
    # [4] = hash of individual ally ship numbers
    offAttackValue = [0]*5
    defAttackValue = [0]*5
    if crd1 >= 90:
      offAttackValue[0] = self.artDef[crd1]
    else:
      offAttackValue[0] = crd1
    if crd2 >= 90:
      defAttackValue[0] = self.artDef[crd2]
    else:
      defAttackValue[0] = crd2

    offAttackValue[4] = {}
    defAttackValue[4] = {}

    ## offense
    aC = 0
    for x in self.players:
      if x == plyr:
        offAttackValue[1] = self.mothership[x]
      else:
        aC += x.shipWorth(self.mothership[x])
        offAttackValue[4][x] = self.mothership[x]
    offAttackValue[2] = aC
    ## defense
    defAttackValue[1] = pNum[2].system.planet[int(pNum[0])].ships[pNum[1]]
    aC = 0
    for x in self.players:
      aC += x.shipWorth(self.carriership[x])
      defAttackValue[4][x] = self.carriership[x]
    defAttackValue[2] = aC

    offAttackValue = plyr.revealMath(offAttackValue)
    defAttackValue = dest.revealMath(defAttackValue)

    for x in self.players:
      if x.mathOverrideSelf:
        if x == plyr:
          offAttackValue = x.powerMath(offAttackValue)
        elif x == dest:
          defAttackValue = x.powerMath(defAttackValue)
      if x.mathOverrideOppo:
        if x == plyr:
          defAttackValue = x.powerMath(defAttackValue)
        elif x == dest:
          offAttackValue = x.powerMath(offAttackValue)

    drawReveal(offAttackValue, defAttackValue)

    return [offAttackValue[3], defAttackValue[3]]

########## Resolution ##########
  def resolution(self, plyr, oppo, res, plan, choice):
    if str(res[0]) == "N" and str(res[1]) == "N":
      successful = self.negotiation(plyr, oppo)
    elif str(res[0]) != "N" and str(res[1]) != "N":
      offWin = res[0] > res[1]
      if plyr.calcWin:
        offWin = plyr.winCalcuation(res)
      if oppo.calcWin:
        offWin = oppo.winCalcuation(res)

      if offWin:
        successful = True
        plyr.winEncounter(plyr, oppo, choice)
        oppo.loseEncounter(plyr, oppo, choice)
      else:
        successful = False
        plyr.loseEncounter(plyr, oppo, choice)
        oppo.winEncounter(plyr, oppo, choice)
    else:
      if str(res[1]) == "N":
        successful = True
        oppo.getCompensation(plyr, choice[2].system.planet[int(choice[0])].ships[oppo])
        plyr.winEncounter(plyr, oppo, choice)
        oppo.loseEncounter(plyr, oppo, choice)
      elif str(res[0]) == "N":
        successful = False
        plyr.getCompensation(oppo, self.mothership[plyr])
        plyr.loseEncounter(plyr, oppo, choice)
        oppo.winEncounter(plyr, oppo, choice)

    plyr.discardUsedECard(plan[0])
    oppo.discardUsedECard(plan[1])
    return successful

  def negotiation(self, plyr, oppo):
    print("You have one minute to make a deal.")
    while 1:
      deal = input("Was the deal successful? [Y/n]: ")
      if deal.lower() == "y" or deal == "":
        print("Success!")
        return True
      elif deal.lower() == "n":
        print("Pick 3 ships to kill")
        draw(self)
        print(plyr.name+">>\t",end='')
        self.carriership[plyr] += plyr.getShips(3, 3)
        print(oppo.name+">>\t",end='')
        self.carriership[oppo] += oppo.getShips(3, 3)

        plyr.killShips(3, self.carriership, plyr)
        oppo.killShips(3, self.carriership, oppo)
        return False
      else:
        print("Try again")

########## End Turn ##########
  def endTurn(self, plyr, success):
    for x in self.players:
      if x.checkWin():
        self.winner = x
        self.gameover = True

    if not plyr.goAgain(success):
      # Increase player index
      self.plyrix += 1
      # Set player index back to 0 if greater than number of players
      if self.plyrix >= len(self.players): self.plyrix = 0

    done = input("Is your name Amanda?: ")
    if done.lower() == "y": self.gameover = True
