class artifact:
  def __init__(self, g, n, sh, *ph):
    self.theGame = g
    self.name    = n
    self.short   = sh
    self.phases  = ph

  def use(self, plyr, crd, other):
    plyr.discardCard(crd)
    work = True
    worked = [work]
    print("BEFORE: "+str(worked[0]))
    for x in self.theGame.players:
      x.checkArtifacts("use card", self.name, worked)
    print("AFTER: "+str(worked[0]))
    return worked[0]
