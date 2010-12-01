from imports.player import *

class machine(player):
  def goAgain(self, success):
    if not self.hasPower or self.zapped:
      return super().goAgain(success)
    else:
      if self.hasEncounterCards():
        while 1:
          again = input("Would you like to have another encounter? [Y/n]: ")
          if again.lower() == "y" or again.lower() == "":
            self.usePower()
            if not self.zapped:
              self.encounterNumber += 1
              return True
            else:
              return super().goAgain(success)
          elif again.lower() == "n":
            self.encounterNumber = 1
            return False
          else:
            print("ERROR: Try again")
      else:
        self.encounterNumber = 1
        return False
