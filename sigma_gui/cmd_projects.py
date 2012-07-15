#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os

import pmq

class CmdProjects( pmq.Actor ) :

  def m_cmd_projects( self ) :
    lProjects = []
    sPath = os.path.expanduser( "~/Documents" )
    for _, lSubdirs, _ in os.walk( sPath ) :
      for sSubdir in lSubdirs :
        for sMark in [ ".hg", ".git", ".svn" ] :
          if os.path.isdir( os.path.join( sPath, sSubdir, sMark ) ) :
            lProjects.append( sSubdir )
            break
      break
    pmq.post( 'm_projects', lProjects )

  def m_project_set( self, i_sName ) :
    pmq.post( 'm_cfg_set', 'current_project', i_sName )

  def m_project_get( self ) :
    pmq.response( pmq.request( 'm_cfg_get', 'current_project' ) )

