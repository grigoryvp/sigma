#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndSettings( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    with pu.Rack( parent = self ) :
      with pu.Shelf() :
        with pu.List() as this :
          this.append( "keybindings", 'keybindings' )
          this.selectByBaton( 'keybindings' )
        with pu.Stack() as this :
          with pu.Rack( 'keybindings') :
            with pu.Label() as this :
              this.setText( "VIM" )
          this.setCurrent( 'keybindings' )
      with pu.Spacer() : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Button( 'settings_cancel' ) as this :
          this.setText( "Cancel" )
        with pu.Button( 'settings_apply' ) as this :
          this.setText( "Apply" )
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Settings" )

  def m_start( self ) :
    sName = "geometry_{0}".format( self.name() )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )

  ##x Overrides |pu.Wnd.show()|.
  def show( self, i_fShow = True ) :
    if i_fShow :
      self.center()
      self.grab_set()
      self.transient( master = self.parent() )
    else :
      self.grab_release()
      self.transient( master = None )
    super( WndSettings, self ).show( i_fShow )

  def m_wndsettings_close( self ) :
    self.show( False )

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.name() )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

  def m_on_settings_cancel( self ) :
    self.show( False )

  def m_on_settings_apply( self ) :
    self.show( False )

