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
      pmq.post( 'm_project_files', [] )
    else :
      pmq.post( 'm_no_project_set' )

  def m_project_file_get( self ) :
    pmq.response( self.m_oFile )

  def m_project_file_set( self, i_oFile ) :
    self.m_oFile = i_oFile

