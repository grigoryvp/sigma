#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import time
import threading

sys.dont_write_bytecode = True

import pmq
import pu

from shutdown import Shutdown
from wnd_editor import WndEditor

Shutdown()
WndEditor()
pmq.post( 'm_wndeditor_show' )
pmq.start( pu.mainLoop, pu.mainLoopStop )

