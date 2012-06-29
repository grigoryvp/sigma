#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os

sys.path.append( "{0}{1}vendor".format( sys.path[ 0 ], os.sep ) )
sys.dont_write_bytecode = True

import sigma_gui

sigma_gui.start()

