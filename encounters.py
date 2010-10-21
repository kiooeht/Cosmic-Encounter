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
  newplayer = macron.macron(n, name, planets, ships, crd)
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

    plyr.regroup()					#regroup
    desCard = plyr.destiny(destiny)	#destiny
    choice = plyr.launch(desCard)	#launch

    #alliances
    ##offense
    offAskPly = []
    if len(players) - 2 > 0:
      print("Offense")
      askHelp = input("Would you like to ask for allies? [Y/n]: ")
      if askHelp.lower() != "n":
        for x in players:
          if x != plyr and x != desCard:
            plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            while plyHelp.lower() != "y" and plyHelp.lower() != "n":
              print("Excuse me, sir/madam, but it appears that you have neglected to specify")
              print("correctly a positive or negative response to my question. If you would")
              print("be so gracious, would you please try again and don't mess up this time.")
              print("Thank you.")
              plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            if plyHelp.lower() == "y":
              offAskPly.append(x)
    ##defense
    defAskPly = []
    if len(players) - 2 > 0:
      print("Defense")
      askHelp = input("Would you like to ask for allies? [Y/n]: ")
      if askHelp.lower() != "n":
        for x in players:
          if x != plyr and x != desCard:
            plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            while plyHelp.lower() != "y" and plyHelp.lower() != "n":
              print("Excuse me, sir/madam, but it appears that you have neglected to specify")
              print("correctly a positive or negative response to my question. If you would")
              print("be so gracious, would you please try again and don't mess up this time.")
              print("Thank you.")
              plyHelp = input("Ask "+x.name+" to be allies? [y/n]: ")
            if plyHelp.lower() == "y":
              defAskPly.append(x)
    ##others
    for x in players:
      if x != plyr and x != desCard:
        x.confirmAlly(plyr, offAskPly, desCard, defAskPly)

    #planning
    ##offense
    print(plyr.name+">>")
    # implement check if only non-encounter cards later
    if len(plyr.hand) <= 0:
      plyr.drawHand(int(cardspp))
      print("Drawing a new hand")
    while 1:
      plyr.showHand()
      selCard = input("Select an encounter card from your hand [0-"+str(len(plyr.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(plyr.hand)-1 and int(selCard) >= 0:
        # implement check for encounter card later
        offCard = plyr.useCard(int(selCard))
        break
      else:
        print("That does not exist in your hand")
    ##defense
    print(desCard.name+">>")
    # implement check if only non-encouner cards later
    if len(desCard.hand) <= 0:
      desCard.drawHand(int(cardspp))
      print("Drawing a new hand")
    while 1:
      desCard.showHand()
      selCard = input("Select an encounter card from your hand [0-"+str(len(desCard.hand)-1)+"]: ")
      if selCard.isdigit() and int(selCard) <= len(desCard.hand)-1 and int(selCard) >= 0:
        # implement check for encounter card later
        defCard = desCard.useCard(int(selCard))
        break
      else:
        print("That does not exist in your hand")

    #reveal
    res = drawReveal(plyr,offCard,desCard,defCard,choice)

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

    cards.discardCard(offCard)
    cards.discardCard(defCard)

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

'''
Things to implement
Not-stupid users
Game play
Artifacts
Powers

TURN PHASES:
1. start turn
2. regroup
3.  destiny
4. attack desisions
5. alliances
6. planning (card choice, power options, etc.)
7. reveal
8. outcome
'''
