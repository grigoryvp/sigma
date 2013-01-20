#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'project files' command implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os
import sys
import subprocess

import pmq


class CmdProjectFiles( pmq.Actor ) :


  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.__oFile = None


  def m_cmd_project_files( self ) :
    oProject = pmq.request( 'm_project_get' )
    if oProject is not None :
      ##! subprocess can't handle unicode.
      sDir = oProject.dir.encode( sys.getfilesystemencoding() )
      for _, lSubdirs, _ in os.walk( oProject.dir ) :
        break
      if ".hg" in lSubdirs :
        lCmd = [ "hg", "status", "-A", "-R", sDir ]
        try :
          sOut = subprocess.check_output( lCmd )
        except subprocess.CalledProcessError :
          return
        lFiles = []
        for sLine in [ s.strip() for s in sOut.split( "\n" ) ] :
          ##  First two characters are modification status flag.
          if len( sLine ) > 2 :
            ##  Not ignored?
            if 'I' != sLine[ 0 ] :
              lFiles.append( sLine[ 2 : ] )
      else :
        return pmq.post( 'm_project_no_vcs' )
      pmq.post( 'm_project_files', lFiles )
    else :
      pmq.post( 'm_no_project_set' )


  def m_project_file_get( self ) :
    pmq.response( self.__oFile )


  def m_project_file_set( self, o_file ) :
    self.__oFile = o_file

