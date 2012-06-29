#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import time
import threading

sys.dont_write_bytecode = True

import pmq
import pu

from shutdown import Shutdown
from cfg import Cfg
from wnd_editor import WndEditor
from commandline import Commandline

def start() :
  Shutdown()
  Cfg()
  Commandline()
  WndEditor()
  ##  Load configuration from file, if any.
  pmq.post( 'm_cfg_load' )
  ##  Let actors request configuration.
  pmq.post( 'm_startup' )
  ##  Depends on command-line args perform different commands and
  ##  display different window.
  pmq.post( 'm_commandline_handle' )
  pmq.start( pu.mainLoop, pu.mainLoopStop )

