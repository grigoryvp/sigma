#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os
if sys.platform == 'linux2' :
  ##! Import before Tkinter, otherwise warnings will arise.
  import gtk.gdk

##! Compatible with install from source code.
sys.path.append( "{0}{1}vendor".format( sys.path[ 0 ], os.sep ) )

import sigma_gui_impl

sigma_gui_impl.start()

