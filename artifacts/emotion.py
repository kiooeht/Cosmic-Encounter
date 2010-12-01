from imports.artifact import *

class emotion(artifact):
  def __init__(self, g):
    super().__init__(g, "Emotion Control", "EC", "reveal")

  def use(self, plyr, crd, other):
    print("Main players must attempt to make a deal")
    worked = super().use(plyr, crd, other)

    if worked:
      res = list(other)[0]
      res[0] = "N"
      res[1] = "N"
