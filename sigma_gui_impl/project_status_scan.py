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
      for _, lSubdirs, _ in os.walk( oProject.dir ) :
        break
      if ".hg" in lSubdirs :
        self.__statusScanHg( oProject )
      else :
        oProject.commited = 'error'
      pmq.post( 'm_project_status_updated', oProject )
    pmq.post( 'm_project_status_scan', delay = 1.0 )

  def __statusScanHg( self, b_oProject ) :
    ##! subprocess can't handle unicode.
    sDir = b_oProject.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "diff", "-R", sDir ]
    try :
      sOut = subprocess.check_output( lCmd )
      if len( sOut.strip() ) > 0 :
        b_oProject.commited = 'no'
      else :
        b_oProject.commited = 'yes'
    except subprocess.CalledProcessError :
      b_oProject.commited = 'error'

  ##  Round robin next project pickup.
  def __nextProject( self ) :
    self.m_nCurrentProject += 1
    if self.m_nCurrentProject >= len( self.m_lProjects ) :
      self.m_nCurrentProject = 0
    if self.m_nCurrentProject < len( self.m_lProjects ) :
      return self.m_lProjects[ self.m_nCurrentProject ]
    return None

