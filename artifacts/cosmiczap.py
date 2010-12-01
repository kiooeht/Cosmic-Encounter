from imports.artifact import *

class cosmiczap(artifact):
  def __init__(self, g):
    super().__init__(g, "Cosmic Zap", "CZ", "power")

  def use(self, plyr, crd, other):
    print(other[0].name + ">> Your power has been Zapped!")
    worked = super().use(plyr, crd, other)

    if worked:
      other[0].zapped = True
