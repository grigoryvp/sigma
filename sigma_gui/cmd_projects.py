#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'projects' command implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os
import sys

import pmq
from model_project import Project


ABOUT_VCS = [ "hg", "git", "svn" ]


class CmdProjects( pmq.Actor ) :


  def __init__( self ) :
    pmq.Actor.__init__( self )
    ##  Current project, for fast access.
    self.__oProject = None


  def m_cmd_projects( self ) :
    lProjects = []
    sEncoding = sys.getfilesystemencoding()
    sPath = os.path.expanduser( "~/Documents" ).decode( sEncoding )
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
            ##  Read mercurial subrepos, if any.
            if 'hg'  == sVcs :
              sHgsub = os.path.join( sProjectDir, ".hgsub" )
              if os.path.isfile( sHgsub ) :
                with open( sHgsub ) as oFile :
                  for sLine in oFile :
                    sSubpath = (sLine.split( "=" ) + [ "" ])[ 0 ].strip()
                    if sSubpath :
                      ##! Mercurial always outputs with '/' separatpr.
                      sSubpath = sSubpath.replace( "/", os.sep )
                      oProject = Project()
                      sName = "{0}{1}{2}".format( sSubdir, os.sep, sSubpath )
                      oProject.name = sName
                      oProject.dir = os.path.join( sProjectDir, sSubpath )
                      oProject.vcs = sVcs
                      lProjects.append( oProject )
            break
      break
    pmq.post( 'm_projects', lProjects )


  def m_project_set( self, o_project ) :
    pmq.post( 'm_cfg_set', 'current_project', o_project.name )
    self.__oProject = o_project


  def m_project_get( self ) :
    if self.__oProject :
      pmq.response( self.__oProject )
      return
    sName = pmq.request( 'm_cfg_get', 'current_project' )
    if not sName :
      pmq.response( None )
      return
    oProject = Project()
    oProject.name = sName
    sEncoding = sys.getfilesystemencoding()
    sDocuments = os.path.expanduser( "~/Documents" ).decode( sEncoding )
    oProject.dir = os.path.join( sDocuments, sName )
    for sVcs in ABOUT_VCS :
      if os.path.isdir( os.path.join( oProject.dir, "." + sVcs ) ) :
        oProject.vcs = sVcs
        self.__oProject = oProject
        pmq.response( oProject )
        break
    else :
      pmq.response( None )

