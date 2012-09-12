#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import time
import threading

import pmq
import pyuser as pu

from shutdown          import Shutdown
from cfg               import Cfg
from wnd_editor        import WndEditor
from wnd_toc           import WndToc
from wnd_settings      import WndSettings
from wnd_projects      import WndProjects
from wnd_project_files import WndProjectFiles
from commandline       import Commandline
from cmd_toc           import CmdToc
from cmd_projects      import CmdProjects
from cmd_project_files import CmdProjectFiles
from editor_vim        import EditorVim
from windows           import Windows

def start() :
  Shutdown()
  Cfg()
  Commandline()
  CmdToc()
  CmdProjects()
  CmdProjectFiles()
  EditorVim()
  Windows()
  oRoot = WndEditor()
  WndToc( oRoot )
  WndProjects( oRoot )
  WndProjectFiles()
  WndSettings( oRoot )
  pmq.start( pu.mainLoop, pu.mainLoopStop )

