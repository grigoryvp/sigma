#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma
# Copyright 2011-2012 Grigory Petrov
# See LICENSE for details.

import argparse

import sigma

oParser = argparse.ArgumentParser( description = "Sigma" )
oParser.add_argument( 'file', help = "File to preprocess." )
oArgs = oParser.parse_args()

sigma.preprocessFile( oArgs.file )

