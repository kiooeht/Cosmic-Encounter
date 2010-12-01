from imports.artifact import *

class cardzap(artifact):
  def __init__(self, g):
    super().__init__(g, "Anti Card", "AC", "use card")

  def use(self, plyr, crd, other):
    print(other[0] + " had been Negated!")
    worked = super().use(plyr, crd, other)

    if worked:
      work = other[1]
      work[0] = False
