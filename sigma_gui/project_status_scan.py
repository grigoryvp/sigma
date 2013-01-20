#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: project status scan implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys
import os
import subprocess

import pmq


class ProjectStatusScan( pmq.Actor ) :


  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.__lProjects = []
    ##  Current project index in |m_lProjects|.
    self.__nCurrentProject = None


  def m_start( self ) :
    pmq.post( 'm_project_status_scan', delay = 1.0 )


  def m_projects( self, l_projects ) :
    self.__lProjects = l_projects


  def m_project_status_scan( self ) :
    if len( self.__lProjects ) > 0 :
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


  def __statusScanHg( self, o_project ) :
    self.__statusScanHgCommit( o_project )
    self.__statusScanHgPush( o_project )
    self.__statusScanHgPull( o_project )


  def __statusScanHgCommit( self, o_project ) :
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
    lCmd = [ "hg", "diff", "-R", sDir ]
    try :
      sOut = subprocess.check_output( lCmd, stderr = subprocess.STDOUT )
      if len( sOut.strip() ) > 0 :
        o_project.commited = 'no'
      else :
        o_project.commited = 'yes'
    except subprocess.CalledProcessError :
      o_project.commited = 'error'


  def __statusScanHgPush( self, o_project ) :
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
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
      o_project.pushed = 'yes'
    elif len( lOut ) > 3 :
      o_project.pushed = 'no'
    else :
      o_project.pushed = 'error'


  def __statusScanHgPull( self, o_project ) :
    ##! subprocess can't handle unicode.
    sDir = o_project.dir.encode( sys.getfilesystemencoding() )
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
      o_project.pulled = 'yes'
    elif len( lOut ) > 3 :
      o_project.pulled = 'no'
    else :
      o_project.pulled = 'error'


  ##  Round robin next project pickup.
  def __nextProject( self ) :
    if self.__nCurrentProject is None :
      self.__nCurrentProject = 0
    else :
      self.__nCurrentProject += 1
    if self.__nCurrentProject >= len( self.__lProjects ) :
      self.__nCurrentProject = 0
    if self.__nCurrentProject < len( self.__lProjects ) :
      return self.__lProjects[ self.__nCurrentProject ]
    return None

