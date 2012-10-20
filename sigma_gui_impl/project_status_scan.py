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
    ##  Current project index in |m_lProjects|.
    self.m_nCurrentProject = None

  def m_start( self ) :
    pmq.post( 'm_project_status_scan', delay = 1.0 )

  def m_projects( self, i_lProjects ) :
    self.m_lProjects = i_lProjects

  def m_project_status_scan( self ) :
    if len( self.m_lProjects ) > 0 :
      oProject = self.__nextProject()
      if oProject is not None :
        for _, lSubdirs, _ in os.walk( oProject.dir ) :
          break
        if ".hg" in lSubdirs :
          self.__statusScanHg( oProject )
        else :
          oProject.commited = 'error'
        pmq.post( 'm_project_status_updated', oProject )
    if not self.isShutdown() :
      pmq.post( 'm_project_status_scan', delay = 1.0 )

  def __statusScanHg( self, b_oProject ) :
    self.__statusScanHgCommit( b_oProject )
    self.__statusScanHgPush( b_oProject )
    self.__statusScanHgPull( b_oProject )

  def __statusScanHgCommit( self, b_oProject ) :
    ##! subprocess can't handle unicode.
    sDir = b_oProject.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "diff", "-R", sDir ]
    try :
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
      if len( sOut.strip() ) > 0 :
        b_oProject.commited = 'no'
      else :
        b_oProject.commited = 'yes'
    except subprocess.CalledProcessError :
      b_oProject.commited = 'error'

  def __statusScanHgPush( self, b_oProject ) :
    ##! subprocess can't handle unicode.
    sDir = b_oProject.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "outgoing", "-R", sDir ]
    try :
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
    except subprocess.CalledProcessError as oEx :
      sOut = oEx.output
    lOut = sOut.split( "\n" )
    for sLine in lOut[ : ] :
      if sLine.startswith( "real URL is" ) :
        lOut.remove( sLine )
    if len( lOut ) >= 3 and "no changes found" in lOut[ 2 ] :
      b_oProject.pushed = 'yes'
    elif len( lOut ) > 3 :
      b_oProject.pushed = 'no'
    else :
      b_oProject.pushed = 'error'

  def __statusScanHgPull( self, b_oProject ) :
    ##! subprocess can't handle unicode.
    sDir = b_oProject.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "incoming", "-R", sDir ]
    try :
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
    except subprocess.CalledProcessError as oEx :
      sOut = oEx.output
    lOut = sOut.split( "\n" )
    for sLine in lOut[ : ] :
      if sLine.startswith( "real URL is" ) :
        lOut.remove( sLine )
    if len( lOut ) >= 3 and "no changes found" in lOut[ 2 ] :
      b_oProject.pulled = 'yes'
    elif len( lOut ) > 3 :
      b_oProject.pulled = 'no'
    else :
      b_oProject.pulled = 'error'

  ##  Round robin next project pickup.
  def __nextProject( self ) :
    if self.m_nCurrentProject is None :
      self.m_nCurrentProject = 0
    else :
      self.m_nCurrentProject += 1
    if self.m_nCurrentProject >= len( self.m_lProjects ) :
      self.m_nCurrentProject = 0
    if self.m_nCurrentProject < len( self.m_lProjects ) :
      return self.m_lProjects[ self.m_nCurrentProject ]
    return None

