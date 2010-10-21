from stuff.player import *

class macron(player):
  def launch(self,dest):
    dest.system.draw()
    choice = input("Pick a planet number: ")
    while not choice.isdigit() or int(choice) > len(dest.system.planet)-1 or int(choice) < 0:
      print("ERROR: YOU SUCK")
      choice = input("Pick a planet number: ")
    #choose ships
    draw()
    if mothership[self] == 0:
      mothership[self] += self.getShips(1,1)
    return choice

  def confirmAlly(self, offP, offAskPly, defP, defAskPly):
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
          mothership[x] = self.getShips(1,1)

          draw()
          print("Ships for Defense")
          carriership[x] = self.getShips(1,1)
        else:
          print("You have chosen to help the ",end='')
          if helping == offP:
            print("Offense ("+helping.name+")")
            draw()
            mothership[x] = self.getShips(1,1)
          else:
            print("Defense ("+helping.name+")")
            draw()
            carriership[x] = self.getShips(1,1)

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0]*4 + aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV

  def shipWorth(self, num):
    return num * 4
