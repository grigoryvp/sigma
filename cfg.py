#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import json

import pmq

class Cfg( pmq.Actor ) :

  CFG_FILE_NAME = "~/.sigma_gui"

  def __init__( self ) :
    super( Cfg, self ).__init__()
    self.m_mGeometry = { 'editor' : None }

  def m_cfg_load( self ) :
    sPath = os.path.expanduser( self.CFG_FILE_NAME )
    if os.path.exists( sPath ) :
      with open( sPath ) as this :
        self.m_mGeometry.update( json.loads( this.read() ) )

  def m_geometry_set( self, i_sName, i_sGeometry ) :
    self.m_mGeometry[ i_sName ] = i_sGeometry

  def m_geometry_get( self, i_sName ) :
    pmq.response( self.m_mGeometry[ i_sName ] )

  def m_stop( self ) :
    with open( os.path.expanduser( self.CFG_FILE_NAME ), 'w' ) as this :
      this.write( json.dumps( self.m_mGeometry ) )

