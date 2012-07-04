#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import time
import threading

import pmq
import pu

from shutdown    import Shutdown
from cfg         import Cfg
from wnd_editor  import WndEditor
from wnd_toc     import WndToc
from commandline import Commandline
from cmd_toc     import CmdToc
from editor_vim  import EditorVim

def start() :
  Shutdown()
  Cfg()
  Commandline()
  CmdToc()
  EditorVim()
  WndEditor()
  WndToc()
  ##  Load configuration from file, if any.
  pmq.post( 'm_cfg_load' )
  ##  Let actors request configuration.
  pmq.post( 'm_startup' )
  ##  Depends on command-line args perform different commands and
  ##  display different window.
  pmq.post( 'm_commandline_handle' )
  pmq.start( pu.mainLoop, pu.mainLoopStop )

