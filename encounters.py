#!/usr/bin/python3.1

import sys
import random
import time

from stuff.globals import *
from stuff.player import *
from stuff.system import *
from stuff.planet import *
from stuff.deck import *
from stuff.drawing import *
from stuff.term import oppts
from powers import virus

poop = virus.virus()
poop.gameSetup()

oppts(sys.argv[1:])


def newPlayer(n, name, planets, ships, crd):
  newplayer = player(n, name, planets, ships, crd)
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

    #regroup
    if plyr.getWarpCount() > 0:
      warp[plyr] -= 1
      mothership[plyr] += 1

    #destiny
    desCard = None
    while 1:
      if len(destiny.cards) == 1:
        print("Reshuffling destiny deck")
      desCard = destiny.drawCard(1)[0]
      destiny.discardCard(desCard)
      print("Destiny card: "+desCard.name)
      if desCard.name == plyr.name:
        attack = input(prompt+"Would you like to attack your own system? [y/N]: ")
        if attack.lower() == "y":
          break
      else:
        break
    print("Attacking "+desCard.name+"'s system")
    #launch
    #pick planet
    desCard.system.draw()
    choice = input("Pick a planet number: ")
    while not choice.isdigit() or int(choice) > len(desCard.system.planet)-1 or int(choice) < 0:
      print("ERROR: YOU SUCK")
      choice = input("Pick a planet number: ")
    #choose ships
    draw()
    if mothership[plyr] != 0:
      mothership[plyr] += plyr.getShips(0,4-mothership[plyr])
    else:
      mothership[plyr] += plyr.getShips(1,4)

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
        helping = None
        offAsked = False
        defAsked = False
        for i in offAskPly:
          if i == x:
            offAsked = True
        for i in defAskPly:
          if i == x:
            defAsked = True
        if offAsked or defAsked:
          while helping == None:
            print(x.name+">>")
            if offAsked and defAsked:
              print("  Both the Offense ("+plyr.name+") and Defense ("+desCard.name+") have asked for your help")
              accept = input("  Would you like to help the Offense, Defense, Both, or Neither? [o/d/b/n]: ")
              if accept.lower() == "o":
                helping = plyr
              elif accept.lower() == "d":
                helping = desCard
              elif accept.lower() == "b":
                helping = "both"
            elif offAsked:
              print("  The Offense ("+plyr.name+") has asked for your help")
              accept = input("  Would you like to help the Offense? [y/n]: ")
              if accept.lower() == "y":
                helping = plyr
            else:
              print("  The Defense ("+desCard.name+") has asked for your help")
              accept = input("  Would you like to help the Defense? [y/n]: ")
              if accept.lower() == "y":
                helping = desCard
            if accept.lower() == "n":
              print("  Helping no one")
              break

          if helping != None:
            helpShips= {}
            if helping == "both":
              print("You have chosen to help both the Offense ("+plyr.name+") and Defense ("+desCard.name+")")
              draw()
              print("Ships for Offense")
              mothership[x] = x.getShips(1,4)

              draw()
              print("Ships for Defense")
              carriership[x] = x.getShips(1,4)
            else:
              print("You have chosen to help the ",end='')
              if helping == plyr:
                print("Offense ("+helping.name+")")
                draw()
                mothership[x] = x.getShips(1,4)
              else:
                print("Defense ("+helping.name+")")
                draw()
                carriership[x] = x.getShips(1,4)

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
