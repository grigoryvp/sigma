#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq
from pd import pd

class WndSettings( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    with pu.Rack( parent = self ) :
      with pu.Shelf() :
        with pu.List() :
          pd.o.append( "keybindings", 'keybindings' )
          pd.o.selectByBaton( 'keybindings' )
          pd.o.setGrow( pu.Grow( cx = False, cy = True ) )
          pd.o.setWidth( pixels = pd.o.maxWidth() )
        with pu.Stack() :
          with pu.Rack( 'keybindings') :
            with pu.Radio( name = 'keys_emacs' ) :
              pd.o.setText( "Emacs" )
            with pu.Radio( name = 'keys_vim' ) :
              pd.o.setText( "Vim" )
          pd.o.setCurrent( 'keybindings' )
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Button( 'settings_cancel' ) :
          pd.o.setText( "Cancel" )
        with pu.Button( 'settings_apply' ) :
          pd.o.setText( "Apply" )
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Settings" )

  def m_start( self ) :
    sName = "geometry_{0}".format( self.dname )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256 + 128, 256 )
    if 'vim' == pmq.request( 'm_cfg_get', 'keys' ) :
      self.o( 'keys_vim' ).setSelected()
    else :
      self.o( 'keys_emacs' ).setSelected()

  ##x Overrides |pu.Wnd.show()|.
  def show( self, i_fShow = True ) :
    if i_fShow :
      self.center()
      self.grab_set()
      self.transient( master = self.dparent )
    else :
      self.grab_release()
      self.transient( master = None )
    super( WndSettings, self ).show( i_fShow )

  def m_wndsettings_close( self ) :
    self.show( False )

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

  def m_on_settings_cancel( self ) :
    self.show( False )

  def m_on_settings_apply( self ) :
    if self.o( 'keys_vim' ).isSelected() :
      pmq.post( 'm_cfg_set', 'keys', 'vim' )
    else :
      pmq.post( 'm_cfg_set', 'keys', 'emacs' )
    self.show( False )

