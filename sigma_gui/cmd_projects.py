#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os

import pmq
from model_project import Project

ABOUT_VCS = [ "hg", "git", "svn" ]

class CmdProjects( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    ##  Current project, for fast access.
    self.m_oProject = None

  def m_cmd_projects( self ) :
    lProjects = []
    sPath = os.path.expanduser( "~/Documents" )
    for _, lSubdirs, _ in os.walk( sPath ) :
      for sSubdir in lSubdirs :
        for sVcs in ABOUT_VCS :
          sProjectDir = os.path.join( sPath, sSubdir )
          if os.path.isdir( os.path.join( sProjectDir, "." + sVcs ) ) :
            oProject = Project()
            oProject.name = sSubdir
            oProject.dir = sProjectDir
            oProject.vcs = sVcs
            lProjects.append( oProject )
            break
      break
    pmq.post( 'm_projects', lProjects )

  def m_project_set( self, i_oProject ) :
    pmq.post( 'm_cfg_set', 'current_project', i_oProject.name )
    self.m_oProject = i_oProject

  def m_project_get( self ) :
    if m_oProject :
      pmq.response( self.m_oProject )
      return
    sName = pmq.request( 'm_cfg_get', 'current_project' )
    oProject = Project()
    oProject.name = sName
    oProject.dir = os.path.join( os.path.expanduser( "~/Documents" ), sName )
    for sVcs in ABOUT_VCS :
      if os.path.isdir( os.path.join( oProject.dir, "." + sVcs ) ) :
        oProject.vcs = sVcs
        self.m_oProject = oProject
        pmq.response( oProject )
        break
    else :
      pmq.response( None )

