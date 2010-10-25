#!/usr/bin/python3.1

import sys
import random
import time

from imports.globals import *
from imports.player import *
from imports.system import *
from imports.planet import *
from imports.deck import *
from imports.drawing import *
from imports.term import oppts
from powers import *

# Call terminal switches check
oppts(sys.argv[1:])

# List of all the power classes, unfortunately it doesn't work when put in globals.py =(
powersList = [antimatter.antimatter,
              clone.clone,
              hacker.hacker,
              machine.machine,
              macron.macron,
              masochist.masochist,
              mite.mite,
              trader.trader,
              tripler.tripler,
              virus.virus,
              warpish.warpish,
              zombie.zombie]

# Create player at the same time adding them to all appropriate global lists
# (players, warp, mothership, carriership, destiny)
def newPlayer(n, name, planets, ships, crd):
  if n == 0:
    newplayer = powersList[0](n, name, planets, ships, crd)
  else:
     newplayer = powersList[9](n, name, planets, ships, crd)
  players.append(newplayer)
  warp[newplayer] = 0
  mothership[newplayer] = 0
  carriership[newplayer] = 0
  for x in range(0,3):
    destiny.addCards([newplayer])
  global numplyrs
  numplyrs += 1

# Main game loop
def main():
  #setup
  gameover = False
  winner = None

  # Use global variables
  global warp
  global players
  global eCards
  global cards
  global destiny

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
    newPlayer(numplyrs, name,int(planets),int(shipspp), int(cardspp))

    # Check if there should be more players
    choice  = input("Add more players? [Y/n]: ")
    if choice.lower() == "n": moreplayers = False

  #start loop
  random.seed(time.gmtime())
  # Random starting player
  plyrix = int(random.random()*len(players))
  while not gameover:
    #start turn
    # Set current player
    plyr = players[plyrix]
    mothership["owner"] = plyr
    # Empty mothership (just in case)
    for x in players:
      mothership[x] = 0
    if plyr.encounterNumber == 1:
      print("Starting player turn:",plyr.name)
    print("Starting new encounter")
    prompt = plyr.name + ">> "

    #regroup
    plyr.regroup()
    #destiny
    desCard = plyr.destiny(destiny)
    #launch
    choice = plyr.launch(desCard)

    if choice == "successful":
      # If any players have 5 colonies, they win
      for x in players:
        if x.checkWin():
          winner = x
          gameover = True
      # Increase player index
      plyrix += 1
      # Set player index back to 0 if greater than number of players
      if plyrix >= len(players): plyrix = 0
      done = input("Is your name Amanda?: ")
      if done.lower() == "y": gameover = True
      # Go to next turn
      continue

    #alliances
    # Offense and defense ask for allies
    offAskPly = plyr.allyAsk(desCard)
    defAskPly = desCard.allyAsk(plyr)
    # Other players confirm
    for x in players:
      if x != plyr and x != desCard:
        x.confirmAlly(plyr, offAskPly, desCard, defAskPly)

    #planning
    plan = plyr.planning(desCard)

    #reveal
    res = drawReveal(plyr,plan[0],desCard,plan[1],choice)

    #resolution
    successful = plyr.resolution(desCard, res, plan, choice)

    #end turn
    # If any players have 5 colonies, they win
    for x in players:
      if x.checkWin():
        winner = x
        gameover = True

    if not plyr.goAgain(successful):
      # Increase player index
      plyrix += 1
      # Set player index back to 0 if greater than number of players
      if plyrix >= len(players): plyrix = 0

    done = input("Is your name Amanda?: ")
    if done.lower() == "y": gameover = True

  #end loop

  #victory
  if winner != None:
    print(winner.name + " has won the game!")

  #players[0].colonize(players[1].system.planet[1],3)
  #players[0].discardCard(4)

  # Print a whole bunch of game stats
  draw()
  printStats()
  players[0].showHand()
  players[1].showHand()
  cards.printDeck()
  destiny.printDeck()

main()
