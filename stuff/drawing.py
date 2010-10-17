import sys

from .globals import *

def draw():
  print("\n", end='')
  for x in players:
    x.system.draw()

def printStats():
  print("Stats           | Ships   Colonies   Planets   Cards  ")
  print("----------------+-------------------------------------")
  for x in players:
    stats = x.getStats()
    print("\t",x.name, end='')
    if len(x.name) < 7: print("\t", end='')
    print("| ", end='')
    sys.stdout.write(str(stats[0]))
    sys.stdout.write("/")
    sys.stdout.write(str(stats[1]))
    print("\t ",stats[2],"\t    ",stats[3],"\t      ",stats[4])
  print("")

def reveal(offP,crd1, defP,crd2,pNum):
  returny_stuff = [None]*2
  print("Offense   Defense")
  print("+----+    +----+")
  print("|    |    |    |")
  print("| ",end='')
  if crd1 == 99:
    print("N ",end='')
    returny_stuff[0] = "N"
  else:
    if crd1 < 10: print("0",end='')
    print(crd1,end='')
    returny_stuff[0] = crd1
  print(" | VS | ",end='')
  if crd2 == 99:
    print("N ",end='')
    returny_stuff[1] = "N"
  else:
    if crd2 < 10: print("0",end='')
    print(crd2,end='')
    returny_stuff[1] = crd2
  print(" |")
  print("|    |    |    |")
  print("+----+    +----+")

  mC = 0
  cC = defP.system.planet[int(pNum)].ships[defP]
  for x in players:
    mC += mothership[x]
    cC += carriership[x]
  if returny_stuff[0] != "N":
    returny_stuff[0] += mC
  if returny_stuff[1] != "N":
    returny_stuff[1] += cC
  while mC > 0 or cC > 0:
    if mC >= 4:
      print(" XXXX",end='')
    else:
      print(" ",end='')
      for x in range(0,mC):
        print("X",end='')
      for x in range(mC,4):
        print(" ",end='')
    mC -= 4
    print("      ",end='')
    if cC >=4:
      print("XXXX")
    else:
      for x in range(0,cC):
        print("X",end='')
      print("")
    cC -= 4
  return returny_stuff
