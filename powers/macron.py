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

  def revealMath(self, aV):
    if aV[0] != "N":
      aV[3] = aV[0]*4 + aV[1] + aV[2]
    else:
      aV[3] = "N"

    return aV
