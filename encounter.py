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

oppts(sys.argv[1:])

def newPlayer(n, name, planets, ships, crd):
  if n == 0:
    newplayer = antimatter.antimatter(n, name, planets, ships, crd)
  else:
     newplayer = virus.virus(n, name, planets, ships, crd)
  players.append(newplayer)
  warp[newplayer] = 0
  mothership[newplayer] = 0
  carriership[newplayer] = 0
  for x in range(0,3):
    destiny.addCards([newplayer])
  global numplyrs
  numplyrs += 1

def main():
  #setup
  gameover = False
  winner = None

  global warp
  global players
  global eCards
  global cards
  global destiny

  mode = "meh"
  while mode.lower() != "b" and mode.lower() != "a" and mode.lower() != "":
    mode = input("Basic or Advanced? [B/a]: ")
  if mode.lower() == "b" or mode.lower() == "":
    planets = input("Planets per player (1-10) [5]: ")
    while not planets.isdigit() or int(planets) > 10 or int(planets) < 1:
      if planets != "":
        print("USER ERROR: That is not an integer between 1 and 10")
        planets = input("Planets per player (1-10) [5]: ")
      else: planets = "5"
    if planets == "": planets = "5"
    shipspp = input("Ships per Planet (1-10) [4]: ")
    while not shipspp.isdigit() or int(shipspp) > 10 or int(shipspp) < 1:
      if shipspp != "":
        print("USER ERROR: That is not an integer between 1 and 10")
        shipspp = input("Ships per Planet (1-10) [4]: ")
      else: shipspp = "4"
    if shipspp == "": shipspp = "4"
    cardspp = input("Initial hand size (1-20) [7]: ")
    while not cardspp.isdigit() or int(cardspp) > 10 or int(cardspp) < 1:
      if cardspp != "":
        print("USER ERROR: That is not an integer between 1 and 10")
        cardspp = input("Initial hand size (1-20) [7]: ")
      else: cardspp = "7"
    if cardspp == "": cardspp = "7"

  moreplayers = True
  names = []
  while moreplayers:
    exist = True
    name = ""
    while exist:
      name = input("New player name: ")

      exist = False
      for x in range(0,len(names)):
        if names[x].lower() == name.lower():
          print("Player name already exists, please pick a new name")
          print("Like Spaghatta Nadle, that would be a cool name")
          print("Too bad it's too long!! HAHA!! =P")
          exist = True
      if len(name) > 7:
        print("Player name too long. Must be 7 characters or less")
        exist = True
      if len(name) < 2:
        print("Player name too short. Must be at least 2 characters long")
        exist = True

    names.append(name)

    if mode == "a":
      planets = input("Planets per player (1-10) [5]: ")
      while not planets.isdigit() or int(planets) > 10 or int(planets) < 1:
        if planets != "":
          print("USER ERROR: That is not an integer between 1 and 10")
          planets = input("Planets per player (1-10) [5]: ")
        else: planets = "5"
      if planets == "": planets = "5"
      shipspp = input("Ships per Planet (1-10) [4]: ")
      while not shipspp.isdigit() or int(shipspp) > 10 or int(shipspp) < 1:
        if shipspp != "":
          print("USER ERROR: That is not an integer between 1 and 10")
          shipspp = input("Ships per Planet (1-10) [4]: ")
        else: shipspp = "4"
      if shipspp == "": shipspp = "4"
      cardspp = input("Initial hand size (1-20) [7]: ")
      while not cardspp.isdigit() or int(cardspp) > 10 or int(cardspp) < 1:
        if cardspp != "":
          print("USER ERROR: That is not an integer between 1 and 10")
          cardspp = input("Initial hand size (1-20) [7]: ")
        else: cardspp = "7"
      if cardspp == "": cardspp = "7"

    newPlayer(numplyrs, name,int(planets),int(shipspp), int(cardspp))

    choice  = input("Add more players? [Y/n]: ")
    if choice.lower() == "n": moreplayers = False

  #start loop
  random.seed(time.gmtime())
  plyrix = int(random.random()*len(players))
  while not gameover:
    #start turn
    plyr   = players[plyrix]
    mothership["owner"] = plyr
    for x in players:
      mothership[x] = 0
    print("Starting player turn:",plyr.name)
    prompt = plyr.name + ">> "

    plyr.regroup()          #regroup
    desCard = plyr.destiny(destiny) #destiny
    choice = plyr.launch(desCard) #launch

    #alliances
    offAskPly = plyr.allyAsk(desCard)
    defAskPly = desCard.allyAsk(plyr)
    for x in players:
      if x != plyr and x != desCard:
        x.confirmAlly(plyr, offAskPly, desCard, defAskPly)

    #planning
    plan = plyr.planning(desCard)

    #reveal
    res = drawReveal(plyr,plan[0],desCard,plan[1],choice)

    #resolution
    if str(res[0]) != "N" and str(res[1]) != "N":
      ## offense win
      if res[0] > res[1]:
        print("yay")
        ## kill defense allies
        for x in players:
          warp[x] += carriership[x]
          carriership[x] = 0
        ## kill defense ships
        warp[desCard] = desCard.system.planet[int(choice)].ships[desCard]
        desCard.system.planet[int(choice)].ships[desCard] = 0
        ## colonize
        plyr.colonize(desCard.system.planet[int(choice)], mothership[plyr])
        mothership[plyr] = 0
        ## return offense allies
        for x in players:
          x.placeShips(mothership[x])
          mothership[x] = 0
      ## defense win
      else:
        print("nay")
        ## kill offense ships/allies
        for x in players:
          warp[x] += mothership[x]
          mothership[x] = 0
        ## return defense allies
        for x in players:
          ## defendor reward
          if carriership[x] > 0:
            x.drawCards(carriership[x])
          x.placeShips(carriership[x])
          carriership[x] = 0
    else:
      ## offense win
      if str(res[1]) == "N":
        print("yay")
        ## compensate
        desCard.getCompensation(plyr, desCard.system.planet[int(choice)].ships[desCard])
        ## kill defense allies
        for x in players:
          warp[x] += carriership[x]
          carriership[x] = 0
        ## kill defense ships
        warp[desCard] = desCard.system.planet[int(choice)].ships[desCard]
        desCard.system.planet[int(choice)].ships[desCard] = 0
        ## colonize
        plyr.colonize(desCard.system.planet[int(choice)], mothership[plyr])
        mothership[plyr] = 0
        ## return offense allies
        for x in players:
          x.placeShips(mothership[x])
          mothership[x] = 0
      ## defense win
      else:
        print("nay")
        ## compensate
        plyr.getCompensation(desCard, mothership[plyr])
        ## kill offense ships
        for x in players:
          warp[x] += mothership[x]
          mothership[x] = 0
        ## return defense allies
        for x in players:
          ## defendor reward
          if carriership[x] > 0:
            x.drawCards(carriership[x])
          x.placeShips(carriership[x])
          carriership[x] = 0

    cards.discardCard(plan[0])
    cards.discardCard(plan[1])

    #end turn
    for x in players:
      if x.getColonies() >= 5:
        winner = x
        gameover = True

    plyrix += 1
    if plyrix >= len(players): plyrix = 0

    done = input("Is your name Amanda?: ")
    if done.lower() == "y": gameover = True

  #end loop

  #victory
  if winner != None:
    print(winner.name + " has won the game!")

  #players[0].colonize(players[1].system.planet[1],3)
  #players[0].discardCard(4)

  draw()
  printStats()
  players[0].showHand()
  players[1].showHand()
  cards.printDeck()
  destiny.printDeck()

main()