import sys

from .planet import *

class system:
  def __init__(self, g, own, plan, spp):
    self.theGame= g
    self.owner  = own
    self.planet = []
    for x in range(0,plan):
      self.planet.append(planet(self.owner, self, spp))

  def getShipCount(self, own):
    n = 0
    for x in self.planet:
      if own in x.ships:
        n += x.ships[own]
    return n

  def draw(self):
    print(self.owner.num, end=' ')
    print(self.owner.name, end='')
    if len(self.owner.name) < 7-1: print("\t", end='')
    print("\t", end='')
    print("|  ", end='')
    for k in range(0,len(self.planet)):
      print(k,"  ", end='')
    sys.stdout.write("\n----------------+")
    for k in range(0,len(self.planet)):
      sys.stdout.write("-----")
    print("\n", end='')

    for x in self.theGame.players:
      print("\t",x.name, end='')
      if len(x.name) < 7: print("\t", end='')
      print("|  ", end='')
      for y in self.planet:
        if x in y.ships:
          print(y.ships[x],"  ", end='')
        else:
          print(0,"  ", end='')
      print("\n", end='')
    print("\n", end='')
