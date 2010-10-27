from imports.deck import *
import powers

warp    = {}
players = []
eCards = [0,              \
          1,              \
          4,4,4,4,        \
          5,              \
          6,6,6,6,6,6,6,  \
          7,              \
          8,8,8,8,8,8,8,  \
          9,              \
          10,10,10,10,    \
          11,             \
          12,12,          \
          13,             \
          14,14,          \
          15,             \
          20,20,          \
          23,             \
          30,             \
          40,             \
          99,99,99,99,99, \
          99,99,99,99,99, \
          99,99,99,99,99]
          # 99 = N
          # 90 - 98 Reserved for Artifacts
cards   = deck(eCards)
destiny = deck()
numplyrs = 0
mothership = {}
carriership = {}

# Create list of all power modules
listPowers = {}
for x in powers.__all__:
  listPowers[x] = __import__(x, globals(), locals(), [], 0)
