#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma
# Copyright 2011-2012 Grigory Petrov
# See LICENSE for details.

from sigma_impl import *

def main() :
  import argparse
  oParser = argparse.ArgumentParser( description = "Sigma" )
  oParser.add_argument( 'file', help = "File to preprocess." )
  oArgs = oParser.parse_args()
  preprocessFile( oArgs.file )

if __name__ == '__main__' :
  main()

