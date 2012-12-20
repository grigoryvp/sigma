#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import subprocess

NAME_SHORT = "sigma"
NAME_FULL = "Sigma"
VER_MAJOR = 0
VER_MINOR = 1
try :
  sDir = os.path.dirname( os.path.abspath( __file__ ) )
  ##! Go one dir up in path, where |.hg| is placed.
  sDir = os.sep.join( sDir.split( os.sep )[ : -1 ] )
  sId = subprocess.check_output( [ 'hg', '-R', sDir, 'id', '-n' ] )
  VER_BUILD = int( sId.strip( '+\n' ) )
except subprocess.CalledProcessError :
  VER_BUILD = 0
VER_TXT = ".".join( map( str, [ VER_MAJOR, VER_MINOR, VER_BUILD ] ) )

