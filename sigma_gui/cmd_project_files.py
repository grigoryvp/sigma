#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os

import pmq

class CmdProjectFiles( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.m_oFile = None

  def m_cmd_project_files( self ) :
    oProject = pmq.request( 'm_project_get' )
    if oProject is not None :
      lFiles = []
      sRoot = os.path.normpath( oProject.dir )
      for sDir, lSubdirs, lSubfiles in os.walk( sRoot ) :
        for sFile in lSubfiles :
          sPath = os.path.normpath( sDir )
          assert sPath.startswith( sRoot )
          lSubpath = sPath[ len( sRoot ) : ].split( os.sep )
          ##  Skip VCS paths.
          if not [ s for s in lSubpath if s in [ ".hg", ".git", ".svn" ] ] :
            lFiles.append( os.path.join( sDir, sFile ) )
      pmq.post( 'm_project_files', lFiles )
    else :
      pmq.post( 'm_no_project_set' )

  def m_project_file_get( self ) :
    pmq.response( self.m_oFile )

  def m_project_file_set( self, i_oFile ) :
    self.m_oFile = i_oFile

