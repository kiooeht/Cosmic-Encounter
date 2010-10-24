from imports.player import *

class machine(player):
  def goAgain(self, success):
    if self.hasEncounterCards():
      while 1:
        again = input("Would you like to have another encounter? [Y/n]: ")
        if again.lower() == "y" or again.lower() == "":
          self.encounterNumber += 1
          return True
        elif again.lower() == "n":
          self.encounterNumber = 1
          return False
        else:
          print("ERROR: Try again")
    else:
      self.encounterNumber = 1
      return False
