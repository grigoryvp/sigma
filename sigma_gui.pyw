#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os

sys.path.append( "{0}{1}vendor".format( sys.path[ 0 ], os.sep ) )
sys.dont_write_bytecode = True

##  Import all local libs here while |dont_write_bytecode| is active.
import sigma
import pmq
import pu

import sigma_gui

sigma_gui.start()

