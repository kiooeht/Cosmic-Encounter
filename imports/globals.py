from imports.deck import *

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
cards   = deck(eCards)
destiny = deck()
numplyrs = 0
mothership = {}
carriership = {}