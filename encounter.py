#!/usr/bin/python3.1

import sys
import random
import time

sys.path.append("./powers")
sys.path.append("./artifacts")
from imports.game import *
from imports.player import *
from imports.system import *
from imports.planet import *
from imports.deck import *
from imports.drawing import *
from imports.term import oppts


# Create player at the same time adding them to all appropriate global lists
# (players, warp, mothership, carriership, destiny)
def newPlayer(theGame, n, name, planets, ships, crd):
  if (theGame.powerOpts == "random"):
    random.seed(time.gmtime())
    youcandothat = False
    while not youcandothat:
      youcandothat = True
      powstr = random.choice(list(theGame.listPowers.keys()))
      print(powstr,end=": ")
      for x in theGame.usedPowers:
        if x == powstr:
          youcandothat = False
          print("already used, try again")
    theGame.usedPowers.append(powstr)
    print("")
  else:
    powstr = theGame.powerOpts
  if (theGame.powerOpts == "nopower"):
    newplayer = player(theGame, n, name, planets, ships, crd)
  else:
    newplayer = getattr(theGame.listPowers[powstr], powstr)(theGame, n, name, planets, ships, crd)

  theGame.players.append(newplayer)
  theGame.warp[newplayer] = 0
  theGame.mothership[newplayer] = 0
  theGame.carriership[newplayer] = 0
  for x in range(0,3):
    theGame.destiny.addCards([newplayer])
  theGame.numplyrs += 1

# Main game loop
def main():
  theGame = game()

  # Call terminal switches check
  oppts(sys.argv[1:], theGame)
  if theGame.powerOpts == "random":
    print("Random powers being used.")
  elif theGame.powerOpts == "nopower":
    print("No powers being used.")
  else:
    print("Power being used: "+theGame.powerOpts)

  #setup
  mode = "meh"
  while mode.lower() != "b" and mode.lower() != "a" and mode.lower() != "":
    mode = input("Basic or Advanced? [B/a]: ")
  # Basic setup mode (All players equal)
  if mode.lower() == "b" or mode.lower() == "":
    # Set planets per player (Default 5)
    planets = input("Planets per player (1-10) [5]: ")
    while not planets.isdigit() or int(planets) > 10 or int(planets) < 1:
      if planets != "":
        print("USER ERROR: That is not an integer between 1 and 10")
        planets = input("Planets per player (1-10) [5]: ")
      else: planets = "5"
    if planets == "": planets = "5"
    # Set ships per planet (Default 4)
    shipspp = input("Ships per Planet (1-10) [4]: ")
    while not shipspp.isdigit() or int(shipspp) > 10 or int(shipspp) < 1:
      if shipspp != "":
        print("USER ERROR: That is not an integer between 1 and 10")
        shipspp = input("Ships per Planet (1-10) [4]: ")
      else: shipspp = "4"
    if shipspp == "": shipspp = "4"
    # Set initial hand size (Default 7)
    cardspp = input("Initial hand size (1-20) [7]: ")
    while not cardspp.isdigit() or int(cardspp) > 20 or int(cardspp) < 1:
      if cardspp != "":
        print("USER ERROR: That is not an integer between 1 and 20")
        cardspp = input("Initial hand size (1-20) [7]: ")
      else: cardspp = "7"
    if cardspp == "": cardspp = "7"

  # Create new players loop
  moreplayers = True
  names = []
  while moreplayers:
    exist = True
    name = ""
    while exist:
      name = input("New player name: ")

      # Make sure inputted name doesn't already exist
      exist = False
      for x in range(0,len(names)):
        if names[x].lower() == name.lower():
          print("Player name already exists, please pick a new name")
          print("Like Spaghatta Nadle, that would be a cool name")
          print("Too bad it's too long!! HAHA!! =P")
          exist = True
      # Name must be between 2 and 7 characters long (inclusive)
      if len(name) > 7:
        print("Player name too long. Must be 7 characters or less")
        exist = True
      if len(name) < 2:
        print("Player name too short. Must be at least 2 characters long")
        exist = True

    names.append(name)

    # Advanced setup mode
    if mode == "a":
      # Set planets per player for this player (Default 5)
      planets = input("Planets per player (1-10) [5]: ")
      while not planets.isdigit() or int(planets) > 10 or int(planets) < 1:
        if planets != "":
          print("USER ERROR: That is not an integer between 1 and 10")
          planets = input("Planets per player (1-10) [5]: ")
        else: planets = "5"
      if planets == "": planets = "5"
      # Set ships per planet for this player (Default 4)
      shipspp = input("Ships per Planet (1-10) [4]: ")
      while not shipspp.isdigit() or int(shipspp) > 10 or int(shipspp) < 1:
        if shipspp != "":
          print("USER ERROR: That is not an integer between 1 and 10")
          shipspp = input("Ships per Planet (1-10) [4]: ")
        else: shipspp = "4"
      if shipspp == "": shipspp = "4"
      # Set initial hand size for this player (Default 7)
      cardspp = input("Initial hand size (1-20) [7]: ")
      while not cardspp.isdigit() or int(cardspp) > 20 or int(cardspp) < 1:
        if cardspp != "":
          print("USER ERROR: That is not an integer between 1 and 20")
          cardspp = input("Initial hand size (1-20) [7]: ")
        else: cardspp = "7"
      if cardspp == "": cardspp = "7"

    # Create new player based on inputted numbers
    newPlayer(theGame, theGame.numplyrs, name, int(planets), int(shipspp), int(cardspp))

    # Check if there should be more players
    choice  = input("Add more players? [Y/n]: ")
    if choice.lower() == "n": moreplayers = False

  theGame.promptPlyrs([])
  #start loop
  random.seed(time.gmtime())
  # Random starting player
  theGame.plyrix = int(random.random()*len(theGame.players))
  while not theGame.gameover:
    #start turn
    # Set current player
    plyr = theGame.players[theGame.plyrix]
    theGame.mothership["owner"] = plyr
    # Empty mothership (just in case)
    for x in theGame.players:
      theGame.mothership[x] = 0
    if plyr.encounterNumber == 1:
      print("Starting player turn:",plyr.name)
    print("Starting new encounter")
    prompt = plyr.name + ">> "

    #regroup
    theGame.regroup(plyr)
    # Artifacts
    for x in theGame.players:
      if x == plyr:
        x.checkArtifacts("start turn")
      else:
        x.checkArtifacts("regroup")
    #destiny
    desCard = theGame.destinyPhase(plyr, theGame.destiny)
    #launch
    choice = theGame.launch(plyr, desCard)
    #after launch
    aftLa = []
    for x in theGame.players:
      aftLa.append(x.afterLaunch(theGame, plyr, desCard, choice))
    for x in aftLa:
      if x != None:
        successful = x

    if successful == "successful":
      theGame.endTurn(plyr, successful)
      # Go to next turn
      continue

    desCard = choice[1]

    #alliances
    # Offense and defense ask for allies
    offAskPly = theGame.allyAsk(plyr, desCard)
    defAskPly = theGame.allyAsk(desCard, plyr)
    # Other players confirm
    for x in theGame.players:
      if x != plyr and x != desCard:
        x.confirmAlly(plyr, offAskPly, desCard, defAskPly)
    # Artifacts
    for x in theGame.players:
      x.checkArtifacts("alliance")

    #planning
    plan = theGame.planning(plyr, desCard)

    #reveal
    res = theGame.reveal(plyr,plan[0],desCard,plan[1],choice)
    # Artifacts
    for x in theGame.players:
      x.checkArtifacts("reveal", res)

    #resolution
    successful = theGame.resolution(plyr, desCard, res, plan, choice)
    # Artifacts
    tempsuccess = [successful]
    for x in theGame.players:
      x.checkArtifacts("resolution", desCard, res, tempsuccess)
    successful = tempsuccess[0]

    #end turn
    theGame.endTurn(plyr, successful)

  #end loop

  #victory
  if theGame.winner != None:
    print(theGame.winner.name + " has won the game!")

  #players[0].colonize(players[1].system.planet[1],3)
  #players[0].discardCard(4)

  # Print a whole bunch of game stats
  draw(theGame)
  printStats(theGame)
  theGame.players[0].showHand()
  theGame.players[1].showHand()
  theGame.cards.printDeck()
  theGame.destiny.printDeck()

main()
