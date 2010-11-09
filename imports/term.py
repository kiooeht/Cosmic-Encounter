import sys
import getopt

def printHelp():
  print("Encounters  Copyright (C) 2010 Tony Moore    <kiooeht@gmail.com>\n\
            Copyright (C) 2010 Keith Pearson <thebukwus@gmail.com>\n\
    This program comes with ABSOLUTELY NO WARRANTY; for details use '-w'.\n\
    \n\
-h\t--help\t\tDisplay this help message.\n\
-w\t--warranty\tDisplay warrenty message.\n\
-p POWER\t\tDefine which power everyone should be.\n\
\t--power=POWER\t\"random\" makes everyone a random power.\n\
-n\t--no-powers\tNo powers are used.")

def printWarranty():
  print("  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY\n\
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT\n\
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM \"AS IS\" WITHOUT WARRANTY\n\
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,\n\
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR\n\
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM\n\
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF\n\
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")

def oppts(argv, theGame):
  try:
    opts, args = getopt.getopt(argv, "hwp:n", ["help", "warranty", "power=", "no-powers"])
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
    else:
      if opt in ("-n", "--no-powers"):
        theGame.powerOpts = "nopower"
      elif opt in ("-p", "--power"):
        if arg.lower() == "random":
          theGame.powerOpts = "random"
        else:
          for x in theGame.listPowers:
            if x == arg.lower():
              theGame.powerOpts = arg.lower()
          if theGame.powerOpts != arg.lower():
            print("Specified power does not exist, defaulting to random powers")
