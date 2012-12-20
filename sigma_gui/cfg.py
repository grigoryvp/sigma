#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os
import json

import pmq

class Cfg( pmq.Actor ) :

  CFG_FILE_NAME = "~/.sigmag"

  def __init__( self ) :
    super( Cfg, self ).__init__()
    self.m_mCfg = {
      ##  Keybindings.
      'keys' : 'emacs'
      }

  def m_startup( self ) :
    sPath = os.path.expanduser( self.CFG_FILE_NAME )
    if os.path.exists( sPath ) :
      with open( sPath ) as this :
        self.m_mCfg.update( json.loads( this.read() ) )

  def m_cfg_set( self, i_sKey, i_sVal ) :
    self.m_mCfg[ i_sKey ] = i_sVal

  def m_cfg_get( self, i_sKey ) :
    if i_sKey in self.m_mCfg :
      pmq.response( self.m_mCfg[ i_sKey ] )
    else :
      pmq.response( None )

  def m_stop( self ) :
    with open( os.path.expanduser( self.CFG_FILE_NAME ), 'w' ) as this :
      this.write( json.dumps( self.m_mCfg ) )

