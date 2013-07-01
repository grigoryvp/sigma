#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'Settings' window implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pmq
from pyedsl import pd
import pyuser as pu


class WndSettings( pu.Wnd ):


  def __init__( self, o_parent = None ):
    pu.Wnd.__init__( self, o_parent = o_parent )
    with pu.Rack( o_parent = self ):
      with pu.Shelf():
        with pu.List():
          pd.o.append( "keybindings", 'keybindings' )
          pd.o.selectByBaton( 'keybindings' )
          pd.o.setGrow( pu.Grow( f_cx = False, f_cy = True ) )
          pd.o.setWidth( n_pixels = pd.o.maxWidth() )
        with pu.Stack():
          with pu.Rack( 'keybindings'):
            with pu.Radio( s_name = 'keys_emacs' ):
              pd.o.setText( "Emacs" )
            with pu.Radio( s_name = 'keys_vim' ):
              pd.o.setText( "Vim" )
          pd.o.setCurrent( 'keybindings' )
      with pu.Shelf():
        with pu.Spacer(): pass
        with pu.Button( 'settings_cancel' ):
          pd.o.setText( "Cancel" )
        with pu.Button( 'settings_apply' ):
          pd.o.setText( "Apply" )
      with pu.StatusBar(): pass
    self.setCaption( "Sigma: Settings" )


  def m_start( self ):
    sName = "geometry_{0}".format( self.dname )
    lGeometry = pmq.request( 'm_cfg_get', sName )
    if lGeometry:
      self.setGeometry( * lGeometry )
    else:
      self.setSize( 256 + 128, 256 )
    if 'vim' == pmq.request( 'm_cfg_get', 'keys' ):
      self.o( 'keys_vim' ).setSelected()
    else:
      self.o( 'keys_emacs' ).setSelected()


  ##x Overrides |pu.Wnd.show()|.
  def show( self, f_show = True ):
    if f_show:
      self.center()
      self.setModal()
    else:
      self.setModal( False )
    super( WndSettings, self ).show( f_show )


  def m_wndsettings_close( self ):
    self.show( False )


  def m_shutdown( self ):
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )


  def m_on_settings_cancel( self ):
    self.show( False )


  def m_on_settings_apply( self ):
    if self.o( 'keys_vim' ).isSelected():
      pmq.post( 'm_cfg_set', 'keys', 'vim' )
    else:
      pmq.post( 'm_cfg_set', 'keys', 'emacs' )
    self.show( False )

