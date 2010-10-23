import sys
import random

class deck:
  def __init__(self,contents=[]):
    self.cards   = contents
    self.discard = []
    random.shuffle(self.cards)

  def drawCard(self,n):
    self.card = []
    for x in range(0,n):
      if len(self.cards) <= 0:
        self.shuffle()
      self.card.append(self.cards.pop())
    return self.card

  def shuffle(self):
    random.shuffle(self.discard)
    self.cards.extend(self.discard)
    self.discard = []

  def discardCard(self,crd):
    self.discard.append(crd)

  def addCards(self,crds):
    self.cards.extend(crds)
    random.shuffle(self.cards)

  def printDeck(self):
    l = len(self.cards)
    print("+----+ D----+")
    print("|    | |    |")
    sys.stdout.write("| ")
    if l > 9: sys.stdout.write(str(l))
    else:
      sys.stdout.write("0")
      sys.stdout.write(str(l))
    sys.stdout.write(" | | ")
    if len(self.discard) > 0:
      if self.discard[len(self.discard)-1] == 99:
        sys.stdout.write("N ")
      else:
        if type(self.discard[len(self.discard)-1]).__name__ != "int":
          if self.discard[len(self.discard)-1].num <= 9:
            sys.stdout.write("0")
          sys.stdout.write(str(self.discard[len(self.discard)-1].num))
        else:
          if self.discard[len(self.discard)-1] <= 9:
            sys.stdout.write("0")
          sys.stdout.write(str(self.discard[len(self.discard)-1]))
    else:
      sys.stdout.write("NA")
    sys.stdout.write(" |")
    print("")
    print("|    | |    |")
    print("+----+ +----+")

  def showDeck(self):
    l = len(self.cards)
    lt = len(self.cards)
    while lt >= 7:
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write(str(x))
        if x < 10: sys.stdout.write("-")
        sys.stdout.write("---+ ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("|    | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("| ")
        if self.cards[x] == 99: sys.stdout.write("N ")
        else:
          if type(self.cards[x]).__name__ != "player":
            if self.cards[x] < 10: sys.stdout.write("0")
            sys.stdout.write(str(self.cards[x]))
          else:
            if self.cards[x].num < 10: sys.stdout.write("0")
            sys.stdout.write(str(self.cards[x].num))
        sys.stdout.write(" | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("|    | ")
      print("")
      for x in range(0+(l-lt),7+(l-lt)):
        sys.stdout.write("+----+ ")
      print("")
      lt -= 7
    if lt != 0:
      for x in range(l-lt,l):
        sys.stdout.write(str(x))
        if x < 10: sys.stdout.write("-")
        sys.stdout.write("---+ ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("|    | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("| ")
        if self.cards[x] == 99: sys.stdout.write("N ")
        else:
          if type(self.cards[x]).__name__ != "player":
            if self.cards[x] < 10: sys.stdout.write("0")
            sys.stdout.write(str(self.cards[x]))
          else:
            if self.cards[x].num < 10: sys.stdout.write("0")
            sys.stdout.write(str(self.cards[x].num))
        sys.stdout.write(" | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("|    | ")
      print("")
      for x in range(l-lt,l):
        sys.stdout.write("+----+ ")
      print("")
