class planet:
  def __init__(self, own, sys, shps):
    self.system   = sys
    self.ships    = {}
    self.ships[own] = shps

  def editShips(self, player, shps):
    if player not in self.ships:
      self.ships[player] = shps
    else:
      self.ships[player] += shps
