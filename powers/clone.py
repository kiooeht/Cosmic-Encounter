from imports.player import *

class clone(player):
  def discardUsedECard(self, crd):
    while 1:
      keep = input(self.name+">> Would you like to keep the encounter card ("+str(crd)+")? [Y/n]: ")
      if keep.lower() == "y" or keep.lower() == "":
        self.getCard(crd)
        break
      elif keep.lower() == "n":
        self.theGame.cards.discardCard(crd)
        break
      else:
        print("ERROR: PICK Y OR N")
