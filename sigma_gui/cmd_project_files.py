#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import sys
import subprocess

import pmq

class CmdProjectFiles( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.m_oFile = None

  def m_cmd_project_files( self ) :
    oProject = pmq.request( 'm_project_get' )
    if oProject is not None :
      ##! subprocess can't handle unicode.
      sDir = oProject.dir.decode( sys.getfilesystemencoding() )
      for _, lSubdirs, _ in os.walk( oProject.dir ) :
        break
      if ".hg" in lSubdirs :
        lCmd = [ "hg", "status", "-A", "-R", sDir ]
        try :
          sOut = subprocess.check_output( lCmd )
        except subprocess.CalledProcessError :
          return
        ##  First two characters are modification status flag.
        lFiles = [ s[ 2: ] for s in sOut.split( "\n" ) ]
      else :
        return pmq.post( 'm_project_no_vcs' )
      pmq.post( 'm_project_files', lFiles )
    else :
      pmq.post( 'm_no_project_set' )

  def m_project_file_get( self ) :
    pmq.response( self.m_oFile )

  def m_project_file_set( self, i_oFile ) :
    self.m_oFile = i_oFile

