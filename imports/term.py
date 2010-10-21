import sys
import getopt

def printHelp():
  print("Encounters  Copyright (C) 2010 Tony Moore    <kiooeht@gmail.com>\n\
            Copyright (C) 2010 Keith Pearson <thebukwus@gmail.com>\n\
    This program comes with ABSOLUTELY NO WARRANTY; for details use '-w'.")

def printWarranty():
  print("  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY\n\
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT\n\
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM \"AS IS\" WITHOUT WARRANTY\n\
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,\n\
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR\n\
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM\n\
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF\n\
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")

def oppts(argv):
  try:
    opts, args = getopt.getopt(argv, "hw", ["help", "warranty"])
  except getopt.GetoptError:
    printHelp()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      printHelp()
      sys.exit()
    elif opt in ("-w", "--warranty"):
      printWarranty()
      sys.exit()
