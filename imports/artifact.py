class artifact:
  def __init__(self, g, n, sh, *ph):
    self.theGame = g
    self.name    = n
    self.short   = sh
    self.phases  = ph

  def use(self, plyr):
    return 0
