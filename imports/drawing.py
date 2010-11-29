import sys

def draw(theGame):
  print("\n", end='')
  for x in theGame.players:
    x.system.draw()

def printStats(theGame):
  print("Stats           | Power      Ships   Colonies   Planets   Cards  ")
  print("----------------+------------------------------------------------")
  for x in theGame.players:
    stats = x.getStats()
    print("\t",x.name, end='')
    if len(x.name) < 7: print("\t", end='')
    print("| ", end='')
    sys.stdout.write(stats[0])
    for x in range(0, 11-len(stats[0])):
      sys.stdout.write(" ")
    sys.stdout.write(str(stats[1]))
    sys.stdout.write("/")
    sys.stdout.write(str(stats[2]))
    print("\t ",stats[3],"\t    ",stats[4],"\t      ",stats[5])
  print("")

def drawReveal(offAttack, defAttack):
  print("Offense   Defense")
  print("+----+    +----+")
  print("|    |    |    |")
  print("| ",end='')
  if offAttack[0] != "N" and offAttack[0] < 10: print("0",end='')
  print(offAttack[0],end='')
  if offAttack[0] == "N": print(" ",end='')
  print(" | VS | ",end='')
  if defAttack[0] != "N" and defAttack[0] < 10: print("0",end='')
  print(defAttack[0],end='')
  if defAttack[0] == "N": print(" ",end='')
  print(" |")
  print("|    |    |    |")
  print("+----+    +----+")

  print(" ",end='')
  for i in range(0,offAttack[1]):
    print("X",end='')
  for i in range(offAttack[1],4):
    print(" ",end='')
  print("      ",end='')
  for i in range(0,defAttack[1]):
    print("X",end='')
  for i in range(defAttack[1],4):
    print(" ",end='')
  print("")

  mC = offAttack[4]
  cC = defAttack[4]
  mCLen = 0
  cCLen = 0
  for x in mC:
    mCLen += mC[x]
  for x in cC:
    cCLen += cC[x]
  while mCLen > 0 or cCLen > 0:
    if mCLen >= 4:
      print(" OOOO",end='')
    else:
      print(" ",end='')
      for x in range(0,mCLen):
        print("O",end='')
      for x in range(mCLen,4):
        print(" ",end='')
    mCLen -= 4
    if mCLen < 0: mCLen = 0
    print("      ",end='')
    if cCLen >=4:
      print("OOOO")
    else:
      for x in range(0,cCLen):
        print("O",end='')
      print("")
    cCLen -= 4
    if cCLen < 0: cCLen = 0

  print("T: ",end='')
  if offAttack[3] != "N" and offAttack[3] < 10 and offAttack[3] >= 0: print("0",end='')
  print(offAttack[3],end='')
  if offAttack[3] != "N" and offAttack[3] < 100 and offAttack[3] >= 0: print(" ",end='')
  print("    T: ",end='')
  if defAttack[3] != "N" and defAttack[3] < 10 and defAttack[3] >= 0: print("0",end='')
  print(defAttack[3])
