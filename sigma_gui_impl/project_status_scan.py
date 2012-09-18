#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os
import subprocess

import pmq


class ProjectStatusScan( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.m_lProjects = []
    self.m_nCurrentProject = 0

  def m_startup( self ) :
    pmq.post( 'm_project_status_scan', delay = 1.0 )

  def m_projects( self, i_lProjects ) :
    self.m_lProjects = i_lProjects

  def m_project_status_scan( self ) :
    oProject = self.__nextProject()
    if oProject is not None :
      ##! subprocess can't handle unicode.
      sDir = oProject.dir.encode( sys.getfilesystemencoding() )
      for _, lSubdirs, _ in os.walk( oProject.dir ) :
        break
      if ".hg" in lSubdirs :
        lCmd = [ "hg", "diff", "-R", sDir ]
        try :
          sOut = subprocess.check_output( lCmd )
          if len( sOut.strip() ) > 0 :
            oProject.commited = 'no'
          else :
            oProject.commited = 'yes'
        except subprocess.CalledProcessError :
          oProject.commited = 'error'
      else :
        oProject.commited = 'error'
      pmq.post( 'm_project_status_updated', oProject )
    pmq.post( 'm_project_status_scan', delay = 1.0 )

  ##  Round robin next project pickup.
  def __nextProject( self ) :
    self.m_nCurrentProject += 1
    if self.m_nCurrentProject >= len( self.m_lProjects ) :
      self.m_nCurrentProject = 0
    if self.m_nCurrentProject < len( self.m_lProjects ) :
      return self.m_lProjects[ self.m_nCurrentProject ]
    return None

