#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: project status scan implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys
import os
import subprocess

import pmq


class ProjectStatusScan( pmq.Actor ):


  def __init__( self ):
    pmq.Actor.__init__( self )
    self._projects_l = []
    ##  Current project index in |m_lProjects|.
    self._currentProject_n = None


  def m_start( self ):
    pmq.post( 'm_project_status_scan', delay = 1.0 )


  def m_projects( self, l_projects ):
    self._projects_l = l_projects


  def m_project_status_scan( self ):
    if len( self._projects_l ) > 0:
      oProject = self._nextProject()
      if oProject is not None:
        for _, lSubdirs, _ in os.walk( oProject.dir ):
          break
        if ".hg" in lSubdirs:
          self._statusScanHg( oProject )
        else:
          oProject.commited = 'error'
        pmq.post( 'm_project_status_updated', oProject )
    if not self.isShutdown():
      pmq.post( 'm_project_status_scan', delay = 1.0 )


  def _statusScanHg( self, o_project ):
    self._statusScanHgCommit( o_project )
    self._statusScanHgPush( o_project )
    self._statusScanHgPull( o_project )


  def _statusScanHgCommit( self, o_project ):
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "diff", "-R", sDir ]
    try:
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
      if len( sOut.strip() ) > 0:
        o_project.commited = 'no'
      else:
        o_project.commited = 'yes'
    except subprocess.CalledProcessError:
      o_project.commited = 'error'


  def _statusScanHgPush( self, o_project ):
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "outgoing", "-R", sDir ]
    try:
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
    except subprocess.CalledProcessError as oEx:
      sOut = oEx.output
    lOut = sOut.split( "\n" )
    for sLine in lOut[ : ]:
      if sLine.startswith( "real URL is" ):
        lOut.remove( sLine )
    if len( lOut ) >= 3 and "no changes found" in lOut[ 2 ]:
      o_project.pushed = 'yes'
    elif len( lOut ) > 3:
      o_project.pushed = 'no'
    else:
      o_project.pushed = 'error'


  def _statusScanHgPull( self, o_project ):
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "incoming", "-R", sDir ]
    try:
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
    except subprocess.CalledProcessError as oEx:
      sOut = oEx.output
    lOut = sOut.split( "\n" )
    for sLine in lOut[ : ] :
      if sLine.startswith( "real URL is" ):
        lOut.remove( sLine )
    if len( lOut ) >= 3 and "no changes found" in lOut[ 2 ]:
      o_project.pulled = 'yes'
    elif len( lOut ) > 3:
      o_project.pulled = 'no'
    else:
      o_project.pulled = 'error'


  ##  Round robin next project pickup.
  def _nextProject( self ):
    if self._currentProject_n is None:
      self._currentProject_n = 0
    else:
      self._currentProject_n += 1
    if self._currentProject_n >= len( self._projects_l ):
      self._currentProject_n = 0
    if self._currentProject_n < len( self._projects_l ):
      return self._projects_l[ self._currentProject_n ]
    return None

