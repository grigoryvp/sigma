#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import sys
import sigma_gui_impl

##  Allows |sigma_gui_impl| to search files in |./res| subfolder.
sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
sigma_gui_impl.start()

