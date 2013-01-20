#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma persistent configuration.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os
import json

import pmq


class Cfg( pmq.Actor ) :


  CFG_FILE_NAME = "~/.sigmag"


  def __init__( self ) :
    super( Cfg, self ).__init__()
    self.__mCfg = {
      ##  Keybindings.
      'keys' : 'emacs'
      }


  def m_startup( self ) :
    sPath = os.path.expanduser( self.CFG_FILE_NAME )
    if os.path.exists( sPath ) :
      with open( sPath ) as this :
        self.__mCfg.update( json.loads( this.read() ) )


  def m_cfg_set( self, s_key, s_val ) :
    self.__mCfg[ s_key ] = s_val


  def m_cfg_get( self, s_key ) :
    if s_key in self.__mCfg :
      pmq.response( self.__mCfg[ s_key ] )
    else :
      pmq.response( None )


  def m_stop( self ) :
    with open( os.path.expanduser( self.CFG_FILE_NAME ), 'w' ) as this :
      this.write( json.dumps( self.__mCfg ) )

