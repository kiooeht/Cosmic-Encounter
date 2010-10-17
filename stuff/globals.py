from stuff.deck import *

warp    = {}
players = []
eCards  = [4,4,     \
       6,6,6,6,6, \
       8,8,8,8,8, \
       10,10,10,  \
       12,12,12,  \
       14,14,14,  \
       18,18,   \
       20,30,2,2, \
       99,99,99]*3
       # 99 = N
cards   = deck(eCards)
destiny = deck()
numplyrs = 0
mothership = {}
carriership = {}
