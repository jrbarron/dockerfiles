#!/usr/bin/python

import os
import sys
import glob
import argparse
from os.path import isfile
from os.path import exists

SYMBOLS_DIR = "/opt/symbols/"

def symbolize(filename):
  basename = os.path.basename(filename)
  symbolFilename = SYMBOLS_DIR + basename + ".sym"
  os.system("dump_syms " + filename + " > " + symbolFilename)
  symbolFile = open(symbolFilename, 'r')
  module = symbolFile.readline().split(" ")
  moduleId =  module[3]
  moduleName = SYMBOLS_DIR + module[4].strip() + "/" + moduleId

  if not exists(moduleName):
    os.makedirs(moduleName)

  os.rename(symbolFilename, moduleName + "/" + basename + ".sym")


if not exists(SYMBOLS_DIR):
  os.mkdir(SYMBOLS_DIR)

if len(sys.argv) > 1:
  target = sys.argv[1]
  if (isfile(target)):
      symbolize(target)
  else:
    for filename in glob.glob(target + '/*.so'):
      symbolize(filename)
else:
  for filename in glob.glob('*.so'):
    symbolize(filename)

